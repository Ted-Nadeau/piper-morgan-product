#!/usr/bin/env python3
"""
Script to add auth tokens to standup API tests
"""
import re

# Read the test file
with open("tests/api/test_standup_api.py", "r") as f:
    lines = f.readlines()

#  Step 1: Add auth_token to function signatures that don't have it
new_lines = []
for line in lines:
    # Match async function definitions with client but no auth_token
    if "async def test_" in line and "client" in line and "auth_token" not in line:
        # Add auth_token parameter after client
        line = line.replace(", mock_standup_result)", ", auth_token, mock_standup_result)")
        line = line.replace(", client)", ", client, auth_token)")
    new_lines.append(line)

# Step 2: Add Authorization headers to client.post calls that don't have them
final_lines = []
i = 0
while i < len(new_lines):
    line = new_lines[i]

    # Check if this line starts a client.post to /generate
    if "response = client.post" in line and "/generate" in line:
        # Collect the full client.post call
        call_lines = [line]
        j = i + 1
        while j < len(new_lines) and ")" not in new_lines[j - 1]:
            call_lines.append(new_lines[j])
            j += 1

        # Check if headers already exist
        full_call = "".join(call_lines)
        if "headers=" not in full_call and "Authorization" not in full_call:
            # Need to add headers
            # Find the line with json={...} closing
            for k, cline in enumerate(call_lines):
                if "json=" in cline:
                    # This is the json parameter line
                    # Look for the closing }
                    m = k
                    while m < len(call_lines):
                        if "}" in call_lines[m]:
                            # Found closing brace
                            indent = len(call_lines[m]) - len(call_lines[m].lstrip())
                            # Check if it ends with ), or just }
                            if call_lines[m].rstrip().endswith("),"):
                                # Already has comma, insert before )
                                call_lines[m] = call_lines[m].replace("),", ",")
                                call_lines.insert(
                                    m + 1,
                                    " " * indent
                                    + 'headers={"Authorization": f"Bearer {auth_token}"}\n',
                                )
                                call_lines.insert(m + 2, " " * (indent - 4) + ")\n")
                            elif call_lines[m].rstrip().endswith(")"):
                                # No comma, add one
                                call_lines[m] = call_lines[m].replace(")", ",")
                                call_lines.insert(
                                    m + 1,
                                    " " * indent
                                    + 'headers={"Authorization": f"Bearer {auth_token}"}\n',
                                )
                                call_lines.insert(m + 2, " " * (indent - 4) + ")\n")
                            else:
                                # Just closing brace, add comma and headers on next line
                                if not call_lines[m].rstrip().endswith(","):
                                    call_lines[m] = call_lines[m].rstrip() + ",\n"
                                call_lines.insert(
                                    m + 1,
                                    " " * indent
                                    + 'headers={"Authorization": f"Bearer {auth_token}"}\n',
                                )
                            break
                        m += 1
                    break

        final_lines.extend(call_lines)
        i = j
    else:
        final_lines.append(line)
        i += 1

# Write back
with open("tests/api/test_standup_api.py", "w") as f:
    f.writelines(final_lines)

print("✅ Added auth tokens to all /generate tests")

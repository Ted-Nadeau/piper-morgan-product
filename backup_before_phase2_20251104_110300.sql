--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: edgetype; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.edgetype AS ENUM (
    'REFERENCES',
    'DEPENDS_ON',
    'IMPLEMENTS',
    'MEASURES',
    'INVOLVES',
    'TRIGGERS',
    'ENHANCES',
    'REPLACES',
    'SUPPORTS',
    'BECAUSE',
    'ENABLES',
    'REQUIRES',
    'PREVENTS',
    'LEADS_TO',
    'BEFORE',
    'DURING',
    'AFTER',
    'CUSTOM'
);


ALTER TYPE public.edgetype OWNER TO piper;

--
-- Name: integrationtype; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.integrationtype AS ENUM (
    'GITHUB',
    'JIRA',
    'LINEAR',
    'SLACK'
);


ALTER TYPE public.integrationtype OWNER TO piper;

--
-- Name: intentcategory; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.intentcategory AS ENUM (
    'EXECUTION',
    'ANALYSIS',
    'SYNTHESIS',
    'STRATEGY',
    'LEARNING',
    'QUERY',
    'CONVERSATION',
    'IDENTITY',
    'TEMPORAL',
    'STATUS',
    'PRIORITY',
    'GUIDANCE',
    'UNKNOWN'
);


ALTER TYPE public.intentcategory OWNER TO piper;

--
-- Name: listtype; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.listtype AS ENUM (
    'PERSONAL',
    'PROJECT',
    'TEAM',
    'TEMPLATE',
    'ARCHIVE'
);


ALTER TYPE public.listtype OWNER TO piper;

--
-- Name: nodetype; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.nodetype AS ENUM (
    'CONCEPT',
    'DOCUMENT',
    'PERSON',
    'ORGANIZATION',
    'TECHNOLOGY',
    'PROCESS',
    'METRIC',
    'EVENT',
    'RELATIONSHIP',
    'CUSTOM'
);


ALTER TYPE public.nodetype OWNER TO piper;

--
-- Name: orderingstrategy; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.orderingstrategy AS ENUM (
    'MANUAL',
    'PRIORITY',
    'DUE_DATE',
    'CREATED_DATE',
    'ALPHABETICAL',
    'STATUS'
);


ALTER TYPE public.orderingstrategy OWNER TO piper;

--
-- Name: taskstatus; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.taskstatus AS ENUM (
    'PENDING',
    'RUNNING',
    'COMPLETED',
    'FAILED',
    'SKIPPED'
);


ALTER TYPE public.taskstatus OWNER TO piper;

--
-- Name: tasktype; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.tasktype AS ENUM (
    'ANALYZE_REQUEST',
    'EXTRACT_REQUIREMENTS',
    'IDENTIFY_DEPENDENCIES',
    'CREATE_WORK_ITEM',
    'UPDATE_WORK_ITEM',
    'NOTIFY_STAKEHOLDERS',
    'GENERATE_DOCUMENT',
    'CREATE_SUMMARY',
    'GITHUB_CREATE_ISSUE',
    'GENERATE_GITHUB_ISSUE_CONTENT',
    'ANALYZE_GITHUB_ISSUE',
    'ANALYZE_FILE',
    'SUMMARIZE',
    'LIST_PROJECTS',
    'EXTRACT_WORK_ITEM',
    'JIRA_CREATE_TICKET',
    'SLACK_SEND_MESSAGE',
    'PROCESS_USER_FEEDBACK'
);


ALTER TYPE public.tasktype OWNER TO piper;

--
-- Name: todopriority; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.todopriority AS ENUM (
    'LOW',
    'MEDIUM',
    'HIGH',
    'URGENT'
);


ALTER TYPE public.todopriority OWNER TO piper;

--
-- Name: todostatus; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.todostatus AS ENUM (
    'PENDING',
    'IN_PROGRESS',
    'COMPLETED',
    'CANCELLED',
    'BLOCKED'
);


ALTER TYPE public.todostatus OWNER TO piper;

--
-- Name: workflowstatus; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.workflowstatus AS ENUM (
    'PENDING',
    'RUNNING',
    'COMPLETED',
    'FAILED',
    'CANCELLED'
);


ALTER TYPE public.workflowstatus OWNER TO piper;

--
-- Name: workflowtype; Type: TYPE; Schema: public; Owner: piper
--

CREATE TYPE public.workflowtype AS ENUM (
    'CREATE_FEATURE',
    'ANALYZE_METRICS',
    'CREATE_TICKET',
    'CREATE_TASK',
    'REVIEW_ITEM',
    'GENERATE_REPORT',
    'PLAN_STRATEGY',
    'LEARN_PATTERN',
    'ANALYZE_FEEDBACK',
    'CONFIRM_PROJECT',
    'SELECT_PROJECT',
    'ANALYZE_FILE',
    'LIST_PROJECTS',
    'MULTI_AGENT'
);


ALTER TYPE public.workflowtype OWNER TO piper;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO piper;

--
-- Name: alpha_users; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.alpha_users (
    id uuid NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    display_name character varying(100),
    password_hash character varying(500),
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    last_login_at timestamp without time zone,
    alpha_wave integer,
    test_start_date timestamp without time zone,
    test_end_date timestamp without time zone,
    migrated_to_prod boolean,
    migration_date timestamp without time zone,
    prod_user_id character varying(255),
    preferences jsonb,
    learning_data jsonb,
    notes text,
    feedback_count integer,
    last_active timestamp without time zone
);


ALTER TABLE public.alpha_users OWNER TO piper;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.audit_logs (
    id character varying(255) NOT NULL,
    user_id character varying(255),
    session_id character varying(255),
    event_type character varying(50) NOT NULL,
    action character varying(100) NOT NULL,
    resource_type character varying(50),
    resource_id character varying(255),
    status character varying(20) NOT NULL,
    severity character varying(20) NOT NULL,
    message text NOT NULL,
    details json,
    ip_address character varying(45),
    user_agent character varying(500),
    request_id character varying(255),
    request_path character varying(500),
    old_value json,
    new_value json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.audit_logs OWNER TO piper;

--
-- Name: features; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.features (
    id character varying NOT NULL,
    product_id character varying,
    name character varying NOT NULL,
    description text,
    hypothesis text,
    acceptance_criteria json,
    status character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.features OWNER TO piper;

--
-- Name: feedback; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.feedback (
    id character varying NOT NULL,
    session_id character varying NOT NULL,
    feedback_type character varying NOT NULL,
    rating integer,
    comment text NOT NULL,
    context json,
    user_id character varying(255),
    conversation_context json,
    source character varying,
    status character varying,
    priority character varying,
    sentiment_score double precision,
    categories json,
    tags json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.feedback OWNER TO piper;

--
-- Name: intents; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.intents (
    id character varying NOT NULL,
    category public.intentcategory,
    action character varying,
    confidence double precision,
    context json,
    original_message text,
    created_at timestamp without time zone,
    workflow_id character varying
);


ALTER TABLE public.intents OWNER TO piper;

--
-- Name: items; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.items (
    id character varying NOT NULL,
    text character varying NOT NULL,
    "position" integer DEFAULT 0 NOT NULL,
    list_id character varying,
    item_type character varying(50) DEFAULT 'item'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.items OWNER TO piper;

--
-- Name: knowledge_edges; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.knowledge_edges (
    id character varying NOT NULL,
    source_node_id character varying NOT NULL,
    target_node_id character varying NOT NULL,
    edge_type public.edgetype NOT NULL,
    weight double precision,
    node_metadata json,
    properties json,
    session_id character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.knowledge_edges OWNER TO piper;

--
-- Name: knowledge_nodes; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.knowledge_nodes (
    id character varying NOT NULL,
    name character varying NOT NULL,
    node_type public.nodetype NOT NULL,
    description text,
    node_metadata json,
    properties json,
    session_id character varying,
    embedding_vector json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.knowledge_nodes OWNER TO piper;

--
-- Name: list_items; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.list_items (
    id character varying NOT NULL,
    list_id character varying NOT NULL,
    item_id character varying NOT NULL,
    item_type character varying NOT NULL,
    "position" integer NOT NULL,
    added_at timestamp without time zone NOT NULL,
    added_by character varying NOT NULL,
    list_priority character varying,
    list_due_date timestamp without time zone,
    list_notes text
);


ALTER TABLE public.list_items OWNER TO piper;

--
-- Name: list_memberships; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.list_memberships (
    id character varying NOT NULL,
    list_id character varying NOT NULL,
    todo_id character varying NOT NULL,
    "position" integer NOT NULL,
    added_at timestamp without time zone NOT NULL,
    added_by character varying NOT NULL,
    list_priority public.todopriority,
    list_due_date timestamp without time zone,
    list_notes text
);


ALTER TABLE public.list_memberships OWNER TO piper;

--
-- Name: lists; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.lists (
    id character varying NOT NULL,
    name character varying NOT NULL,
    description text,
    item_type character varying NOT NULL,
    list_type character varying NOT NULL,
    ordering_strategy character varying NOT NULL,
    color character varying(7),
    emoji character varying(4),
    is_archived boolean NOT NULL,
    is_default boolean NOT NULL,
    list_metadata json,
    tags jsonb,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    owner_id character varying NOT NULL,
    shared_with jsonb,
    item_count integer NOT NULL,
    completed_count integer NOT NULL
);


ALTER TABLE public.lists OWNER TO piper;

--
-- Name: personality_profiles; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.personality_profiles (
    id uuid NOT NULL,
    user_id character varying(255) NOT NULL,
    warmth_level double precision NOT NULL,
    confidence_style character varying(50) NOT NULL,
    action_orientation character varying(50) NOT NULL,
    technical_depth character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.personality_profiles OWNER TO piper;

--
-- Name: products; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.products (
    id character varying NOT NULL,
    name character varying NOT NULL,
    vision text,
    strategy text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.products OWNER TO piper;

--
-- Name: project_integrations; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.project_integrations (
    id character varying NOT NULL,
    project_id character varying NOT NULL,
    type public.integrationtype NOT NULL,
    name character varying NOT NULL,
    config json NOT NULL,
    is_active boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.project_integrations OWNER TO piper;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.projects (
    id character varying NOT NULL,
    name character varying NOT NULL,
    description text,
    is_default boolean,
    is_archived boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.projects OWNER TO piper;

--
-- Name: stakeholders; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.stakeholders (
    id character varying NOT NULL,
    name character varying NOT NULL,
    email character varying,
    role character varying,
    interests json,
    influence_level integer,
    satisfaction double precision,
    created_at timestamp without time zone
);


ALTER TABLE public.stakeholders OWNER TO piper;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.tasks (
    id character varying NOT NULL,
    workflow_id character varying,
    name character varying NOT NULL,
    type public.tasktype,
    status public.taskstatus,
    input_data json,
    output_data json,
    result json,
    error text,
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.tasks OWNER TO piper;

--
-- Name: todo_lists; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.todo_lists (
    id character varying NOT NULL,
    name character varying NOT NULL,
    description text,
    list_type public.listtype NOT NULL,
    ordering_strategy public.orderingstrategy NOT NULL,
    color character varying(7),
    emoji character varying(4),
    is_archived boolean NOT NULL,
    is_default boolean NOT NULL,
    list_metadata json,
    tags jsonb,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    owner_id character varying NOT NULL,
    shared_with jsonb,
    todo_count integer NOT NULL,
    completed_count integer NOT NULL
);


ALTER TABLE public.todo_lists OWNER TO piper;

--
-- Name: todos; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.todos (
    id character varying NOT NULL,
    title character varying NOT NULL,
    description text,
    status public.todostatus NOT NULL,
    priority public.todopriority NOT NULL,
    parent_id character varying,
    "position" integer NOT NULL,
    due_date timestamp without time zone,
    reminder_date timestamp without time zone,
    scheduled_date timestamp without time zone,
    tags jsonb,
    project_id character varying,
    context character varying,
    estimated_minutes integer,
    actual_minutes integer,
    completion_notes text,
    list_metadata json,
    knowledge_node_id character varying,
    related_todos json,
    creation_intent character varying,
    intent_confidence double precision,
    external_refs jsonb,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    completed_at timestamp without time zone,
    owner_id character varying NOT NULL,
    assigned_to character varying
);


ALTER TABLE public.todos OWNER TO piper;

--
-- Name: token_blacklist; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.token_blacklist (
    id integer NOT NULL,
    token_id character varying(255) NOT NULL,
    user_id character varying(255),
    reason character varying(50) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.token_blacklist OWNER TO piper;

--
-- Name: token_blacklist_id_seq; Type: SEQUENCE; Schema: public; Owner: piper
--

CREATE SEQUENCE public.token_blacklist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_blacklist_id_seq OWNER TO piper;

--
-- Name: token_blacklist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: piper
--

ALTER SEQUENCE public.token_blacklist_id_seq OWNED BY public.token_blacklist.id;


--
-- Name: uploaded_files; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.uploaded_files (
    id character varying NOT NULL,
    session_id character varying NOT NULL,
    filename character varying(500) NOT NULL,
    file_type character varying(255),
    file_size integer,
    storage_path character varying(1000),
    upload_time timestamp without time zone,
    last_referenced timestamp without time zone,
    reference_count integer,
    file_metadata json,
    item_metadata json
);


ALTER TABLE public.uploaded_files OWNER TO piper;

--
-- Name: user_api_keys; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.user_api_keys (
    id integer NOT NULL,
    user_id character varying(255) NOT NULL,
    provider character varying(50) NOT NULL,
    key_reference character varying(500) NOT NULL,
    is_active boolean NOT NULL,
    is_validated boolean,
    last_validated_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by character varying(255),
    previous_key_reference character varying(500),
    rotated_at timestamp without time zone
);


ALTER TABLE public.user_api_keys OWNER TO piper;

--
-- Name: user_api_keys_id_seq; Type: SEQUENCE; Schema: public; Owner: piper
--

CREATE SEQUENCE public.user_api_keys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_api_keys_id_seq OWNER TO piper;

--
-- Name: user_api_keys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: piper
--

ALTER SEQUENCE public.user_api_keys_id_seq OWNED BY public.user_api_keys.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.users (
    id character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(500),
    role character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    last_login_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO piper;

--
-- Name: work_items; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.work_items (
    id character varying NOT NULL,
    product_id character varying,
    feature_id character varying,
    title character varying NOT NULL,
    description text,
    type character varying,
    status character varying,
    priority character varying,
    labels json,
    assignee character varying,
    project_id character varying,
    source_system character varying,
    external_id character varying,
    external_url character varying,
    item_metadata json,
    external_refs json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.work_items OWNER TO piper;

--
-- Name: workflows; Type: TABLE; Schema: public; Owner: piper
--

CREATE TABLE public.workflows (
    id character varying NOT NULL,
    type public.workflowtype,
    status public.workflowstatus,
    input_data json,
    output_data json,
    context json,
    result json,
    error text,
    intent_id character varying(255),
    created_at timestamp without time zone,
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.workflows OWNER TO piper;

--
-- Name: token_blacklist id; Type: DEFAULT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.token_blacklist ALTER COLUMN id SET DEFAULT nextval('public.token_blacklist_id_seq'::regclass);


--
-- Name: user_api_keys id; Type: DEFAULT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.user_api_keys ALTER COLUMN id SET DEFAULT nextval('public.user_api_keys_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.alembic_version (version_num) FROM stdin;
40fc95f25017
\.


--
-- Data for Name: alpha_users; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.alpha_users (id, username, email, display_name, password_hash, is_active, is_verified, created_at, updated_at, last_login_at, alpha_wave, test_start_date, test_end_date, migrated_to_prod, migration_date, prod_user_id, preferences, learning_data, notes, feedback_count, last_active) FROM stdin;
3f4593ae-5bc9-468d-b08d-8c4c02a5b963	xian	xian@test.local	Xian	$2b$12$NBmaBktcB5XmXz.0UNe/3OdXy/R.jTdltRWrFsCvTRnqiiUz5Emhm	t	t	2025-11-01 14:45:37.713439	2025-11-03 18:45:54.502241	2025-11-03 18:45:54.500237	1	2025-11-01 07:45:37.712463	\N	f	\N	\N	{"calendar": {"key_dates": {"2025-08-11": "MCP Monday Sprint completed", "2025-08-12": "Enhanced standup experience target", "2025-08-15": "UX improvement validation", "2025-08-18": "Next development sprint planning"}, "daily_routines": {"06:00": "Daily standup with Piper Morgan", "09:00": "Development focus time", "14:00": "UX and improvement work", "17:00": "Documentation and handoff preparation"}, "recurring_meetings": {"Friday": "Pattern review and methodology validation", "Monday": "MCP development sprints", "Wednesday": "UX enhancement sessions"}}, "projects": [{"name": "VA/Decision Reviews Q4 Onramp", "role": "Director of Product Management", "team": "DRAGONS", "focus": "VA decision review system onramp for Q4 2025", "status": "Active development and implementation", "company": "Kind Systems", "allocation": 70, "next_milestone": "Q4 onramp completion and system validation"}, {"name": "Piper Morgan AI Assistant", "phase": "UX enhancement and conversational AI improvement", "status": "Production-ready MCP Consumer with real GitHub integration", "allocation": 25, "achievements": ["2,480 lines of production code", "84 real GitHub issues retrieved"], "next_milestone": "Enhanced standup experience with PIPER.md context"}, {"name": "OneJob/Content/Other", "focus": "Core functionality, technical writing, pattern documentation", "status": "Ongoing maintenance and development", "allocation": 5}], "priorities": [{"goal": "Complete VA decision review system for Q4 2025", "name": "VA Q4 Onramp system implementation and delivery", "rank": 1, "success": "System operational and validated for production use", "timeline": "Q4 2025 completion"}, {"goal": "Successful integration and collaboration with company team", "name": "Kind Systems and DRAGONS team collaboration", "rank": 2, "success": "Effective team coordination and project delivery", "timeline": "Ongoing throughout Q4"}, {"goal": "Apply consolidated patterns to new development", "name": "Pattern application and validation", "rank": 3, "success": "Consistent architecture and implementation quality", "timeline": "Ongoing"}, {"goal": "Improve overall conversational AI experience", "name": "UX enhancement and user experience", "rank": 4, "success": "Natural language workflows and context awareness", "timeline": "Q4 2025"}, {"goal": "Maintain comprehensive and accurate documentation", "name": "Documentation and knowledge management", "rank": 5, "success": "All links working, up-to-date guides", "timeline": "Ongoing"}], "user_context": {"name": "Christian", "role": "Product Manager / Developer", "location": "San Francisco Bay Area", "timezone": "Pacific Time (PT)", "working_hours": "6:00 AM - 6:00 PM PT", "communication_style": "Direct, efficiency-focused, pattern-oriented"}, "current_focus": {"quarter": "Q4 2025", "week_priority": "VA deliverables and onramp system implementation", "strategic_goal": "Successfully launch VA decision review system for Q4 2025", "primary_objective": "VA/Decision Reviews Q4 Onramp implementation and delivery"}, "key_initiatives": [{"name": "VA Q4 Onramp", "status": "ACTIVE", "description": "VA decision review system implementation"}, {"name": "Kind Systems Integration", "status": "ACTIVE", "description": "Company and DRAGONS team collaboration"}, {"name": "Director of PM Role", "status": "ACTIVE", "description": "Product management leadership responsibilities"}, {"name": "Piper Morgan AI", "status": "COMPLETE", "description": "Production-ready MCP Consumer delivered"}], "success_metrics": ["VA Q4 Onramp delivery: On-time completion and system validation", "Kind Systems collaboration: Successful DRAGONS team integration", "Director of PM effectiveness: Leadership and strategic delivery", "Piper Morgan AI performance: <150ms target (achieving 36.43ms)"], "knowledge_sources": {"key_resources": ["MCP Foundation: 15,457+ lines of MCP infrastructure code", "Excellence Flywheel: Verify First, Evidence Required, Complete Bookending", "Dual-Agent Coordination: Validated patterns for complex tasks", "GitHub Integration: Real-time issue tracking and management"], "core_documentation": ["docs/patterns/PATTERN-INDEX.md - Master index of 25+ patterns", "docs/architecture/ - System design and implementation patterns", "docs/user-guides/ - Conversational AI and usage patterns", "docs/development/session-logs/ - Development history"], "recent_achievements": ["MCP Consumer: 2,480 lines of production-ready code", "Performance: 36.43ms response time (target: <150ms)", "Integration: 84 real GitHub issues retrieved", "Documentation: Complete deployment and implementation guides"]}, "migration_metadata": {"issue": "#280 CORE-ALPHA-DATA-LEAK", "source": "config/PIPER.md.backup-20251101", "migrated_by": "scripts/migrate_personal_data_to_xian.py", "migration_date": "2025-11-01"}, "key_characteristics": ["Values systematic approaches and evidence-based development", "Prefers quick wins and iterative improvement", "Maintains high standards for code quality and documentation", "Uses GitHub-first tracking for project management", "Emphasizes the Excellence Flywheel methodology"]}	{}	Test user created for Issue #280 development	0	\N
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.audit_logs (id, user_id, session_id, event_type, action, resource_type, resource_id, status, severity, message, details, ip_address, user_agent, request_id, request_path, old_value, new_value, created_at, updated_at) FROM stdin;
ca0fe532-e3c7-4705-9897-bd6345861285	9ddce16a-4e8e-4135-aeeb-bf3c737dc3a7	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "716978d1-187a-41ff-b0c5-597594cab420", "reason": "logout", "expires_at": "2025-11-01T19:55:04"}	127.0.0.1	python-httpx/0.27.2	\N	/auth/logout	null	null	2025-11-01 19:25:04.87502	2025-11-01 19:25:04.87502
353138f3-44bc-471c-b44f-3a2f2b790371	7c6d150b-fe01-4acd-9f29-8b2a38f794b3	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "adac2f22-ff6b-4fcf-857d-ed20c3ef8b4a", "reason": "logout", "expires_at": "2025-11-01T19:55:29"}	127.0.0.1	python-httpx/0.27.2	\N	/auth/logout	null	null	2025-11-01 19:25:29.823692	2025-11-01 19:25:29.823693
4bf9f29e-877c-4052-ae45-4a5a5bed2536	3f4593ae-5bc9-468d-b08d-8c4c02a5b963	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "2a0a0493-23f2-4493-b2a1-b119a76a1c8d", "reason": "logout", "expires_at": "2025-11-01T20:23:23"}	127.0.0.1	curl/8.7.1	\N	/auth/logout	null	null	2025-11-01 19:53:23.14103	2025-11-01 19:53:23.141031
e32c93aa-e934-48a7-8bc7-711a1b750edf	3f4593ae-5bc9-468d-b08d-8c4c02a5b963	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "0314196d-3941-41ba-a36c-ed77d2298bac", "reason": "logout", "expires_at": "2025-11-01T20:25:51"}	127.0.0.1	curl/8.7.1	\N	/auth/logout	null	null	2025-11-01 19:55:51.610181	2025-11-01 19:55:51.610182
022b6684-8add-44ae-aa67-8aeedf21f017	ab25f5e9-0bad-44a1-8232-529a80e3821a	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "3e0aca72-4198-4c08-b78c-67f8ca601ba9", "reason": "logout", "expires_at": "2025-11-01T20:26:26"}	127.0.0.1	python-httpx/0.27.2	\N	/auth/logout	null	null	2025-11-01 19:56:27.004022	2025-11-01 19:56:27.004027
882a3bbf-5a8e-46fd-ad30-53e33edac1fd	293d4b83-4891-4323-ba99-30e7054e9c09	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "35b795b8-b2c2-450a-aae3-5ea1fbb130c5", "reason": "logout", "expires_at": "2025-11-01T20:27:07"}	127.0.0.1	python-httpx/0.27.2	\N	/auth/logout	null	null	2025-11-01 19:57:07.856806	2025-11-01 19:57:07.856807
9bb7019e-2054-4003-89d1-dad7f28a34c3	f3a3b159-9ed1-4773-b2a2-60e334215046	\N	auth	token_revoked	auth	\N	success	info	JWT token revoked: logout	{"token_id": "fce3b963-b012-4864-97f2-84661d717574", "reason": "logout", "expires_at": "2025-11-01T20:27:55"}	127.0.0.1	python-httpx/0.27.2	\N	/auth/logout	null	null	2025-11-01 19:57:55.540305	2025-11-01 19:57:55.540306
\.


--
-- Data for Name: features; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.features (id, product_id, name, description, hypothesis, acceptance_criteria, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.feedback (id, session_id, feedback_type, rating, comment, context, user_id, conversation_context, source, status, priority, sentiment_score, categories, tags, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: intents; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.intents (id, category, action, confidence, context, original_message, created_at, workflow_id) FROM stdin;
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.items (id, text, "position", list_id, item_type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: knowledge_edges; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.knowledge_edges (id, source_node_id, target_node_id, edge_type, weight, node_metadata, properties, session_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: knowledge_nodes; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.knowledge_nodes (id, name, node_type, description, node_metadata, properties, session_id, embedding_vector, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: list_items; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.list_items (id, list_id, item_id, item_type, "position", added_at, added_by, list_priority, list_due_date, list_notes) FROM stdin;
\.


--
-- Data for Name: list_memberships; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.list_memberships (id, list_id, todo_id, "position", added_at, added_by, list_priority, list_due_date, list_notes) FROM stdin;
\.


--
-- Data for Name: lists; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.lists (id, name, description, item_type, list_type, ordering_strategy, color, emoji, is_archived, is_default, list_metadata, tags, created_at, updated_at, owner_id, shared_with, item_count, completed_count) FROM stdin;
\.


--
-- Data for Name: personality_profiles; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.personality_profiles (id, user_id, warmth_level, confidence_style, action_orientation, technical_depth, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.products (id, name, vision, strategy, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: project_integrations; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.project_integrations (id, project_id, type, name, config, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.projects (id, name, description, is_default, is_archived, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: stakeholders; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.stakeholders (id, name, email, role, interests, influence_level, satisfaction, created_at) FROM stdin;
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.tasks (id, workflow_id, name, type, status, input_data, output_data, result, error, started_at, completed_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: todo_lists; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.todo_lists (id, name, description, list_type, ordering_strategy, color, emoji, is_archived, is_default, list_metadata, tags, created_at, updated_at, owner_id, shared_with, todo_count, completed_count) FROM stdin;
\.


--
-- Data for Name: todos; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.todos (id, title, description, status, priority, parent_id, "position", due_date, reminder_date, scheduled_date, tags, project_id, context, estimated_minutes, actual_minutes, completion_notes, list_metadata, knowledge_node_id, related_todos, creation_intent, intent_confidence, external_refs, created_at, updated_at, completed_at, owner_id, assigned_to) FROM stdin;
\.


--
-- Data for Name: token_blacklist; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.token_blacklist (id, token_id, user_id, reason, expires_at, created_at) FROM stdin;
\.


--
-- Data for Name: uploaded_files; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.uploaded_files (id, session_id, filename, file_type, file_size, storage_path, upload_time, last_referenced, reference_count, file_metadata, item_metadata) FROM stdin;
\.


--
-- Data for Name: user_api_keys; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.user_api_keys (id, user_id, provider, key_reference, is_active, is_validated, last_validated_at, created_at, updated_at, created_by, previous_key_reference, rotated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.users (id, username, email, password_hash, role, is_active, is_verified, created_at, updated_at, last_login_at) FROM stdin;
\.


--
-- Data for Name: work_items; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.work_items (id, product_id, feature_id, title, description, type, status, priority, labels, assignee, project_id, source_system, external_id, external_url, item_metadata, external_refs, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: workflows; Type: TABLE DATA; Schema: public; Owner: piper
--

COPY public.workflows (id, type, status, input_data, output_data, context, result, error, intent_id, created_at, started_at, completed_at, updated_at) FROM stdin;
\.


--
-- Name: token_blacklist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: piper
--

SELECT pg_catalog.setval('public.token_blacklist_id_seq', 3, true);


--
-- Name: user_api_keys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: piper
--

SELECT pg_catalog.setval('public.user_api_keys_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: alpha_users alpha_users_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.alpha_users
    ADD CONSTRAINT alpha_users_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: features features_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.features
    ADD CONSTRAINT features_pkey PRIMARY KEY (id);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: intents intents_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.intents
    ADD CONSTRAINT intents_pkey PRIMARY KEY (id);


--
-- Name: knowledge_edges knowledge_edges_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.knowledge_edges
    ADD CONSTRAINT knowledge_edges_pkey PRIMARY KEY (id);


--
-- Name: knowledge_nodes knowledge_nodes_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.knowledge_nodes
    ADD CONSTRAINT knowledge_nodes_pkey PRIMARY KEY (id);


--
-- Name: list_items list_items_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.list_items
    ADD CONSTRAINT list_items_pkey PRIMARY KEY (id);


--
-- Name: list_memberships list_memberships_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.list_memberships
    ADD CONSTRAINT list_memberships_pkey PRIMARY KEY (id);


--
-- Name: lists lists_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.lists
    ADD CONSTRAINT lists_pkey PRIMARY KEY (id);


--
-- Name: personality_profiles personality_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.personality_profiles
    ADD CONSTRAINT personality_profiles_pkey PRIMARY KEY (id);


--
-- Name: personality_profiles personality_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.personality_profiles
    ADD CONSTRAINT personality_profiles_user_id_key UNIQUE (user_id);


--
-- Name: items pk_items; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT pk_items PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: project_integrations project_integrations_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.project_integrations
    ADD CONSTRAINT project_integrations_pkey PRIMARY KEY (id);


--
-- Name: projects projects_name_key; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_name_key UNIQUE (name);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: stakeholders stakeholders_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.stakeholders
    ADD CONSTRAINT stakeholders_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: todo_lists todo_lists_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.todo_lists
    ADD CONSTRAINT todo_lists_pkey PRIMARY KEY (id);


--
-- Name: todos todos_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.todos
    ADD CONSTRAINT todos_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist token_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.token_blacklist
    ADD CONSTRAINT token_blacklist_pkey PRIMARY KEY (id);


--
-- Name: uploaded_files uploaded_files_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.uploaded_files
    ADD CONSTRAINT uploaded_files_pkey PRIMARY KEY (id);


--
-- Name: user_api_keys uq_user_provider; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.user_api_keys
    ADD CONSTRAINT uq_user_provider UNIQUE (user_id, provider);


--
-- Name: user_api_keys user_api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.user_api_keys
    ADD CONSTRAINT user_api_keys_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: work_items work_items_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.work_items
    ADD CONSTRAINT work_items_pkey PRIMARY KEY (id);


--
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- Name: idx_alpha_users_alpha_wave; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_alpha_users_alpha_wave ON public.alpha_users USING btree (alpha_wave);


--
-- Name: idx_alpha_users_email; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_alpha_users_email ON public.alpha_users USING btree (email);


--
-- Name: idx_alpha_users_last_active; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_alpha_users_last_active ON public.alpha_users USING btree (last_active) WHERE (last_active IS NOT NULL);


--
-- Name: idx_alpha_users_migrated; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_alpha_users_migrated ON public.alpha_users USING btree (migrated_to_prod);


--
-- Name: idx_alpha_users_prod_user; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_alpha_users_prod_user ON public.alpha_users USING btree (prod_user_id) WHERE (prod_user_id IS NOT NULL);


--
-- Name: idx_alpha_users_username; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_alpha_users_username ON public.alpha_users USING btree (username);


--
-- Name: idx_audit_action; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_action ON public.audit_logs USING btree (action);


--
-- Name: idx_audit_event_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_event_type ON public.audit_logs USING btree (event_type);


--
-- Name: idx_audit_ip; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_ip ON public.audit_logs USING btree (ip_address);


--
-- Name: idx_audit_request; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_request ON public.audit_logs USING btree (request_id);


--
-- Name: idx_audit_resource; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_resource ON public.audit_logs USING btree (resource_type, resource_id);


--
-- Name: idx_audit_session; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_session ON public.audit_logs USING btree (session_id);


--
-- Name: idx_audit_severity; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_severity ON public.audit_logs USING btree (severity);


--
-- Name: idx_audit_status; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_status ON public.audit_logs USING btree (status);


--
-- Name: idx_audit_user_date; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_audit_user_date ON public.audit_logs USING btree (user_id, created_at);


--
-- Name: idx_edges_session; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_edges_session ON public.knowledge_edges USING btree (session_id);


--
-- Name: idx_edges_source; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_edges_source ON public.knowledge_edges USING btree (source_node_id);


--
-- Name: idx_edges_source_target; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_edges_source_target ON public.knowledge_edges USING btree (source_node_id, target_node_id);


--
-- Name: idx_edges_target; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_edges_target ON public.knowledge_edges USING btree (target_node_id);


--
-- Name: idx_edges_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_edges_type ON public.knowledge_edges USING btree (edge_type);


--
-- Name: idx_feedback_created_at; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_created_at ON public.feedback USING btree (created_at);


--
-- Name: idx_feedback_rating; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_rating ON public.feedback USING btree (rating);


--
-- Name: idx_feedback_session_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_session_id ON public.feedback USING btree (session_id);


--
-- Name: idx_feedback_source; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_source ON public.feedback USING btree (source);


--
-- Name: idx_feedback_status; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_status ON public.feedback USING btree (status);


--
-- Name: idx_feedback_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_type ON public.feedback USING btree (feedback_type);


--
-- Name: idx_feedback_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_feedback_user_id ON public.feedback USING btree (user_id);


--
-- Name: idx_files_filename; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_files_filename ON public.uploaded_files USING btree (filename);


--
-- Name: idx_files_session; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_files_session ON public.uploaded_files USING btree (session_id, upload_time);


--
-- Name: idx_items_created; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_items_created ON public.items USING btree (created_at);


--
-- Name: idx_items_item_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_items_item_type ON public.items USING btree (item_type);


--
-- Name: idx_items_list_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_items_list_id ON public.items USING btree (list_id);


--
-- Name: idx_items_list_position; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_items_list_position ON public.items USING btree (list_id, "position");


--
-- Name: idx_list_items_added_by; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_list_items_added_by ON public.list_items USING btree (added_by);


--
-- Name: idx_list_items_item_id_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_list_items_item_id_type ON public.list_items USING btree (item_id, item_type);


--
-- Name: idx_list_items_list_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_list_items_list_id ON public.list_items USING btree (list_id);


--
-- Name: idx_list_items_position; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_list_items_position ON public.list_items USING btree (list_id, "position");


--
-- Name: idx_lists_default; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_lists_default ON public.lists USING btree (owner_id, item_type, is_default);


--
-- Name: idx_lists_owner_archived; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_lists_owner_archived ON public.lists USING btree (owner_id, is_archived);


--
-- Name: idx_lists_owner_list_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_lists_owner_list_type ON public.lists USING btree (owner_id, list_type);


--
-- Name: idx_lists_owner_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_lists_owner_type ON public.lists USING btree (owner_id, item_type);


--
-- Name: idx_lists_shared; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_lists_shared ON public.lists USING gin (shared_with);


--
-- Name: idx_lists_tags; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_lists_tags ON public.lists USING gin (tags);


--
-- Name: idx_membership_added_at; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_added_at ON public.list_memberships USING btree (added_at);


--
-- Name: idx_membership_added_by; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_added_by ON public.list_memberships USING btree (added_by);


--
-- Name: idx_membership_list; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_list ON public.list_memberships USING btree (list_id);


--
-- Name: idx_membership_list_due; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_list_due ON public.list_memberships USING btree (list_id, list_due_date);


--
-- Name: idx_membership_list_position; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_list_position ON public.list_memberships USING btree (list_id, "position");


--
-- Name: idx_membership_list_priority; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_list_priority ON public.list_memberships USING btree (list_id, list_priority);


--
-- Name: idx_membership_todo; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_membership_todo ON public.list_memberships USING btree (todo_id);


--
-- Name: idx_nodes_name; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_nodes_name ON public.knowledge_nodes USING btree (name);


--
-- Name: idx_nodes_session; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_nodes_session ON public.knowledge_nodes USING btree (session_id);


--
-- Name: idx_nodes_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_nodes_type ON public.knowledge_nodes USING btree (node_type);


--
-- Name: idx_personality_profiles_action; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_personality_profiles_action ON public.personality_profiles USING btree (action_orientation);


--
-- Name: idx_personality_profiles_active; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_personality_profiles_active ON public.personality_profiles USING btree (is_active);


--
-- Name: idx_personality_profiles_confidence; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_personality_profiles_confidence ON public.personality_profiles USING btree (confidence_style);


--
-- Name: idx_personality_profiles_technical; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_personality_profiles_technical ON public.personality_profiles USING btree (technical_depth);


--
-- Name: idx_personality_profiles_user_active; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_personality_profiles_user_active ON public.personality_profiles USING btree (user_id, is_active);


--
-- Name: idx_personality_profiles_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_personality_profiles_user_id ON public.personality_profiles USING btree (user_id);


--
-- Name: idx_personality_profiles_warmth; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_personality_profiles_warmth ON public.personality_profiles USING btree (warmth_level);


--
-- Name: idx_todo_lists_default; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todo_lists_default ON public.todo_lists USING btree (owner_id, is_default);


--
-- Name: idx_todo_lists_owner_archived; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todo_lists_owner_archived ON public.todo_lists USING btree (owner_id, is_archived);


--
-- Name: idx_todo_lists_owner_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todo_lists_owner_type ON public.todo_lists USING btree (owner_id, list_type);


--
-- Name: idx_todo_lists_shared; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todo_lists_shared ON public.todo_lists USING gin (shared_with);


--
-- Name: idx_todo_lists_tags; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todo_lists_tags ON public.todo_lists USING gin (tags);


--
-- Name: idx_todos_assigned_status; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_assigned_status ON public.todos USING btree (assigned_to, status);


--
-- Name: idx_todos_context; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_context ON public.todos USING btree (context);


--
-- Name: idx_todos_creation_intent; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_creation_intent ON public.todos USING btree (creation_intent);


--
-- Name: idx_todos_due_date; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_due_date ON public.todos USING btree (due_date);


--
-- Name: idx_todos_external_refs; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_external_refs ON public.todos USING gin (external_refs);


--
-- Name: idx_todos_knowledge_node; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_knowledge_node ON public.todos USING btree (knowledge_node_id);


--
-- Name: idx_todos_owner_created; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_owner_created ON public.todos USING btree (owner_id, created_at);


--
-- Name: idx_todos_owner_due; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_owner_due ON public.todos USING btree (owner_id, due_date);


--
-- Name: idx_todos_owner_priority; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_owner_priority ON public.todos USING btree (owner_id, priority);


--
-- Name: idx_todos_owner_status; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_owner_status ON public.todos USING btree (owner_id, status);


--
-- Name: idx_todos_owner_updated; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_owner_updated ON public.todos USING btree (owner_id, updated_at);


--
-- Name: idx_todos_parent; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_parent ON public.todos USING btree (parent_id);


--
-- Name: idx_todos_parent_position; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_parent_position ON public.todos USING btree (parent_id, "position");


--
-- Name: idx_todos_project; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_project ON public.todos USING btree (project_id);


--
-- Name: idx_todos_reminder; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_reminder ON public.todos USING btree (reminder_date);


--
-- Name: idx_todos_scheduled; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_scheduled ON public.todos USING btree (scheduled_date);


--
-- Name: idx_todos_tags; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_todos_tags ON public.todos USING gin (tags);


--
-- Name: idx_token_blacklist_expires; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_token_blacklist_expires ON public.token_blacklist USING btree (expires_at);


--
-- Name: idx_token_blacklist_token_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_token_blacklist_token_id ON public.token_blacklist USING btree (token_id);


--
-- Name: idx_token_blacklist_user_expires; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_token_blacklist_user_expires ON public.token_blacklist USING btree (user_id, expires_at);


--
-- Name: idx_token_blacklist_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_token_blacklist_user_id ON public.token_blacklist USING btree (user_id);


--
-- Name: idx_unique_list_todo; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_unique_list_todo ON public.list_memberships USING btree (list_id, todo_id);


--
-- Name: idx_user_api_keys_active; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_user_api_keys_active ON public.user_api_keys USING btree (is_active);


--
-- Name: idx_user_api_keys_provider; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_user_api_keys_provider ON public.user_api_keys USING btree (provider);


--
-- Name: idx_user_api_keys_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_user_api_keys_user_id ON public.user_api_keys USING btree (user_id);


--
-- Name: idx_users_active; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX idx_users_active ON public.users USING btree (is_active);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: idx_users_username; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX idx_users_username ON public.users USING btree (username);


--
-- Name: ix_alpha_users_email; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX ix_alpha_users_email ON public.alpha_users USING btree (email);


--
-- Name: ix_alpha_users_username; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX ix_alpha_users_username ON public.alpha_users USING btree (username);


--
-- Name: ix_audit_logs_action; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_action ON public.audit_logs USING btree (action);


--
-- Name: ix_audit_logs_event_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_event_type ON public.audit_logs USING btree (event_type);


--
-- Name: ix_audit_logs_ip_address; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_ip_address ON public.audit_logs USING btree (ip_address);


--
-- Name: ix_audit_logs_request_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_request_id ON public.audit_logs USING btree (request_id);


--
-- Name: ix_audit_logs_resource_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_resource_id ON public.audit_logs USING btree (resource_id);


--
-- Name: ix_audit_logs_resource_type; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_resource_type ON public.audit_logs USING btree (resource_type);


--
-- Name: ix_audit_logs_session_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_session_id ON public.audit_logs USING btree (session_id);


--
-- Name: ix_audit_logs_severity; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_severity ON public.audit_logs USING btree (severity);


--
-- Name: ix_audit_logs_status; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_status ON public.audit_logs USING btree (status);


--
-- Name: ix_audit_logs_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_audit_logs_user_id ON public.audit_logs USING btree (user_id);


--
-- Name: ix_feedback_session_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_feedback_session_id ON public.feedback USING btree (session_id);


--
-- Name: ix_feedback_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_feedback_user_id ON public.feedback USING btree (user_id);


--
-- Name: ix_token_blacklist_expires_at; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_token_blacklist_expires_at ON public.token_blacklist USING btree (expires_at);


--
-- Name: ix_token_blacklist_token_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX ix_token_blacklist_token_id ON public.token_blacklist USING btree (token_id);


--
-- Name: ix_token_blacklist_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_token_blacklist_user_id ON public.token_blacklist USING btree (user_id);


--
-- Name: ix_user_api_keys_user_id; Type: INDEX; Schema: public; Owner: piper
--

CREATE INDEX ix_user_api_keys_user_id ON public.user_api_keys USING btree (user_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: piper
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: alpha_users alpha_users_prod_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.alpha_users
    ADD CONSTRAINT alpha_users_prod_user_id_fkey FOREIGN KEY (prod_user_id) REFERENCES public.users(id);


--
-- Name: features features_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.features
    ADD CONSTRAINT features_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: feedback feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: intents intents_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.intents
    ADD CONSTRAINT intents_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- Name: knowledge_edges knowledge_edges_source_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.knowledge_edges
    ADD CONSTRAINT knowledge_edges_source_node_id_fkey FOREIGN KEY (source_node_id) REFERENCES public.knowledge_nodes(id);


--
-- Name: knowledge_edges knowledge_edges_target_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.knowledge_edges
    ADD CONSTRAINT knowledge_edges_target_node_id_fkey FOREIGN KEY (target_node_id) REFERENCES public.knowledge_nodes(id);


--
-- Name: list_items list_items_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.list_items
    ADD CONSTRAINT list_items_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.lists(id);


--
-- Name: list_memberships list_memberships_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.list_memberships
    ADD CONSTRAINT list_memberships_list_id_fkey FOREIGN KEY (list_id) REFERENCES public.todo_lists(id);


--
-- Name: list_memberships list_memberships_todo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.list_memberships
    ADD CONSTRAINT list_memberships_todo_id_fkey FOREIGN KEY (todo_id) REFERENCES public.todos(id);


--
-- Name: personality_profiles personality_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.personality_profiles
    ADD CONSTRAINT personality_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: project_integrations project_integrations_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.project_integrations
    ADD CONSTRAINT project_integrations_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: tasks tasks_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- Name: todos todos_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.todos
    ADD CONSTRAINT todos_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.todos(id);


--
-- Name: todos todos_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.todos
    ADD CONSTRAINT todos_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: work_items work_items_feature_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.work_items
    ADD CONSTRAINT work_items_feature_id_fkey FOREIGN KEY (feature_id) REFERENCES public.features(id);


--
-- Name: work_items work_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: piper
--

ALTER TABLE ONLY public.work_items
    ADD CONSTRAINT work_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- PostgreSQL database dump complete
--

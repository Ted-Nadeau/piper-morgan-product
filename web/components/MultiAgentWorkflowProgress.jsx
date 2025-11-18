/**
 * MultiAgentWorkflowProgress - PM-033d UI Component
 * Displays real-time progress of multi-agent workflow coordination
 */

import React, { useState, useEffect, useCallback } from 'react';
import './MultiAgentWorkflowProgress.css';

const MultiAgentWorkflowProgress = ({
  workflowId,
  workflowName,
  agents = [],
  tasks = [],
  onWorkflowComplete,
  autoRefresh = true
}) => {
  const [workflowState, setWorkflowState] = useState('initializing');
  const [agentStates, setAgentStates] = useState({});
  const [taskProgress, setTaskProgress] = useState({});
  const [performanceMetrics, setPerformanceMetrics] = useState({});
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Performance targets for PM-033d
  const PERFORMANCE_TARGETS = {
    agentCoordination: 50,      // ms
    workflowParsing: 100,       // ms
    taskDistribution: 75,       // ms
    progressUpdates: 25,        // ms
    overallWorkflow: 200        // ms
  };

  // Initialize workflow state
  useEffect(() => {
    if (workflowId && agents.length > 0) {
      initializeWorkflow();
    }
  }, [workflowId, agents]);

  // Auto-refresh functionality
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      refreshWorkflowStatus();
    }, 1000); // Update every second

    return () => clearInterval(interval);
  }, [autoRefresh, workflowId]);

  const initializeWorkflow = useCallback(async () => {
    setWorkflowState('initializing');

    try {
      // Simulate workflow initialization
      await new Promise(resolve => setTimeout(resolve, 100));

      // Initialize agent states
      const initialAgentStates = {};
      agents.forEach(agent => {
        initialAgentStates[agent.id] = {
          status: 'ready',
          currentTasks: 0,
          completedTasks: 0,
          health: 'healthy',
          lastSeen: new Date()
        };
      });

      // Initialize task progress
      const initialTaskProgress = {};
      tasks.forEach(task => {
        initialTaskProgress[task.id] = {
          status: 'pending',
          assignedAgent: null,
          startTime: null,
          estimatedDuration: task.estimatedDuration || 1000,
          progress: 0
        };
      });

      setAgentStates(initialAgentStates);
      setTaskProgress(initialTaskProgress);
      setWorkflowState('ready');

      // Start workflow execution
      setTimeout(() => executeWorkflow(), 200);

    } catch (error) {
      console.error('Workflow initialization failed:', error);
      setWorkflowState('error');
    }
  }, [workflowId, agents, tasks]);

  const executeWorkflow = useCallback(async () => {
    setWorkflowState('executing');

    try {
      // Simulate workflow execution with multiple agents
      const executionSteps = [
        { name: 'Agent Coordination', duration: 50, target: PERFORMANCE_TARGETS.agentCoordination },
        { name: 'Workflow Parsing', duration: 100, target: PERFORMANCE_TARGETS.workflowParsing },
        { name: 'Task Distribution', duration: 75, target: PERFORMANCE_TARGETS.taskDistribution },
        { name: 'Progress Updates', duration: 25, target: PERFORMANCE_TARGETS.progressUpdates }
      ];

      let totalExecutionTime = 0;

      for (const step of executionSteps) {
        const startTime = Date.now();

        // Update progress for this step
        setTaskProgress(prev => {
          const updated = { ...prev };
          Object.keys(updated).forEach(taskId => {
            if (updated[taskId].status === 'pending') {
              updated[taskId].status = 'in_progress';
              updated[taskId].assignedAgent = agents[Math.floor(Math.random() * agents.length)].id;
              updated[taskId].startTime = new Date();
            }
          });
          return updated;
        });

        // Simulate step execution
        await new Promise(resolve => setTimeout(resolve, step.duration));

        const stepDuration = Date.now() - startTime;
        totalExecutionTime += stepDuration;

        // Update performance metrics
        setPerformanceMetrics(prev => ({
          ...prev,
          [step.name.toLowerCase().replace(/\s+/g, '_')]: {
            actual: stepDuration,
            target: step.target,
            targetMet: stepDuration <= step.target
          }
        }));
      }

      // Complete workflow
      setWorkflowState('completed');
      setTaskProgress(prev => {
        const updated = { ...prev };
        Object.keys(updated).forEach(taskId => {
          updated[taskId].status = 'completed';
          updated[taskId].progress = 100;
        });
        return updated;
      });

      if (onWorkflowComplete) {
        onWorkflowComplete({
          workflowId,
          totalExecutionTime,
          performanceMetrics: performanceMetrics,
          success: true
        });
      }

    } catch (error) {
      console.error('Workflow execution failed:', error);
      setWorkflowState('error');
    }
  }, [workflowId, agents, tasks, onWorkflowComplete]);

  const refreshWorkflowStatus = useCallback(async () => {
    try {
      // Simulate status refresh
      setLastUpdate(new Date());

      // Update agent states (simulate real-time updates)
      setAgentStates(prev => {
        const updated = { ...prev };
        Object.keys(updated).forEach(agentId => {
          const agent = updated[agentId];
          if (agent.status === 'ready' || agent.status === 'busy') {
            // Simulate agent activity
            agent.lastSeen = new Date();
            if (Math.random() > 0.8) {
              agent.currentTasks = Math.min(agent.currentTasks + 1, 3);
              agent.status = agent.currentTasks > 0 ? 'busy' : 'ready';
            }
          }
        });
        return updated;
      });

      // Update task progress
      setTaskProgress(prev => {
        const updated = { ...prev };
        Object.keys(updated).forEach(taskId => {
          const task = updated[taskId];
          if (task.status === 'in_progress' && task.progress < 100) {
            // Simulate task progress
            task.progress = Math.min(task.progress + Math.random() * 20, 100);
            if (task.progress >= 100) {
              task.status = 'completed';
            }
          }
        });
        return updated;
      });

    } catch (error) {
      console.error('Status refresh failed:', error);
    }
  }, []);

  const getWorkflowStatusColor = () => {
    switch (workflowState) {
      case 'initializing': return '#f39c12';
      case 'ready': return '#3498db';
      case 'executing': return '#e74c3c';
      case 'completed': return '#27ae60';
      case 'error': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  const getWorkflowStatusIcon = () => {
    switch (workflowState) {
      case 'initializing': return '⏳';
      case 'ready': return '✅';
      case 'executing': return '🔄';
      case 'completed': return '🎉';
      case 'error': return '❌';
      default: return '❓';
    }
  };

  const getPerformanceStatus = (metricName) => {
    const metric = performanceMetrics[metricName];
    if (!metric) return { status: 'pending', color: '#95a5a6' };

    if (metric.targetMet) {
      return { status: 'target_met', color: '#27ae60' };
    } else {
      return { status: 'target_exceeded', color: '#e74c3c' };
    }
  };

  return (
    <div className="multi-agent-workflow-progress">
      {/* Header */}
      <div className="workflow-header">
        <h2 className="workflow-title">
          {getWorkflowStatusIcon()} {workflowName || `Workflow ${workflowId}`}
        </h2>
        <div className="workflow-status">
          <span
            className="status-indicator"
            style={{ backgroundColor: getWorkflowStatusColor() }}
          >
            {workflowState.toUpperCase()}
          </span>
          <span className="last-update">
            Last update: {lastUpdate.toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="performance-metrics">
        <h3>Performance Targets (PM-033d)</h3>
        <div className="metrics-grid">
          {Object.entries(PERFORMANCE_TARGETS).map(([key, target]) => {
            const status = getPerformanceStatus(key);
            return (
              <div key={key} className="metric-card">
                <div className="metric-name">{key.replace(/([A-Z])/g, ' $1').trim()}</div>
                <div className="metric-target">{target}ms</div>
                <div className="metric-status" style={{ color: status.color }}>
                  {status.status === 'pending' ? '⏳' :
                   status.status === 'target_met' ? '✅' : '❌'}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Agent Status */}
      <div className="agent-status-section">
        <h3>Agent Status ({agents.length} agents)</h3>
        <div className="agents-grid">
          {agents.map(agent => {
            const agentState = agentStates[agent.id] || {};
            return (
              <div key={agent.id} className="agent-card">
                <div className="agent-header">
                  <span className="agent-name">{agent.name}</span>
                  <span className={`agent-status ${agentState.status}`}>
                    {agentState.status}
                  </span>
                </div>
                <div className="agent-details">
                  <div>Tasks: {agentState.currentTasks || 0}</div>
                  <div>Completed: {agentState.completedTasks || 0}</div>
                  <div>Health: {agentState.health || 'unknown'}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Task Progress */}
      <div className="task-progress-section">
        <h3>Task Progress ({tasks.length} tasks)</h3>
        <div className="tasks-list">
          {tasks.map(task => {
            const taskState = taskProgress[task.id] || {};
            return (
              <div key={task.id} className="task-item">
                <div className="task-info">
                  <span className="task-name">{task.name}</span>
                  <span className={`task-status ${taskState.status}`}>
                    {taskState.status}
                  </span>
                </div>
                <div className="task-progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${taskState.progress || 0}%` }}
                  />
                </div>
                <div className="task-details">
                  {taskState.assignedAgent && (
                    <span>Agent: {taskState.assignedAgent}</span>
                  )}
                  {taskState.startTime && (
                    <span>Started: {taskState.startTime.toLocaleTimeString()}</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Controls */}
      <div className="workflow-controls">
        <button
          onClick={refreshWorkflowStatus}
          disabled={workflowState === 'completed' || workflowState === 'error'}
          className="refresh-btn"
        >
          🔄 Refresh Status
        </button>
        {workflowState === 'error' && (
          <button onClick={initializeWorkflow} className="retry-btn">
            🔄 Retry Workflow
          </button>
        )}
      </div>
    </div>
  );
};

export default MultiAgentWorkflowProgress;

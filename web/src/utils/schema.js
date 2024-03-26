export const getDataSchema = (path) => {
  if (path[0].startsWith("trace")) {
    switch (path[path.length - 1]) {
      case "batch_instance.csv":
        return [
          ["instance_name", "Instance Name", 300],
          ["task_name", "Task Name", 200],
          ["job_name", "Job Name", 100],
          ["task_type", "Task Type", 100],
          ["status", "Status", 200],
          ["start_time", "Start Time", 100],
          ["end_time", "End Time", 100],
          ["plan_cpu", "Plan CPU", 100],
          ["plan_mem", "Plan Mem", 100],
          ["cpu_avg", "CPU Avg", 100],
          ["cpu_max", "CPU Max", 100],
          ["mem_avg", "Mem Avg", 100],
          ["mem_max", "Mem Max", 100],
        ];
      case "batch_task.csv":
        return [
          ["task_name", "Task Name", 300],
          ["instance_num", "Instance Num", 100],
          ["job_name", "Job Name", 200],
          ["task_type", "Task Type", 100],
          ["status", "Status", 200],
          ["start_time", "Start Time", 200],
          ["end_time", "End Time", 200],
          ["plan_cpu", "Plan CPU", 100],
          ["plan_mem", "Plan Mem", 100],
        ];
      case "container_meta.csv":
        return [
          ["container_id", "Container ID", 200],
          ["machine_id", "Machine ID", 200],
          ["time_stamp", "Time Stamp", 200],
          ["app_du", "App Du", 200],
          ["status", "Status", 200],
          ["cpu_request", "CPU Request", 200],
          ["cpu_limit", "CPU Limit", 200],
          ["mem_size", "Mem Size", 200],
        ];
      case "container_usage.csv":
        return [
          ["container_id", "Container ID", 200],
          ["machine_id", "Machine ID", 200],
          ["time_stamp", "Time Stamp", 200],
          ["cpu_util_percent", "CPU Util Percent", 200],
          ["mem_util_percent", "Mem Util Percent", 200],
          ["cpi", "CPI", 200],
          ["mem_gps", "Mem GPS", 200],
          ["mpki", "MPKI", 200],
          ["net_in", "Net In", 200],
          ["net_out", "Net Out", 200],
          ["disk_io_percent", "Disk IO Percent", 200],
        ];
      case "machine_meta.csv":
        return [
          ["machine_id", "Machine ID", 200],
          ["time_stamp", "Time Stamp", 200],
          ["failure_domain_1", "Failure Domain 1", 200],
          ["failure_domain_2", "Failure Domain 2", 200],
          ["cpu_num", "CPU Num", 200],
          ["mem_size", "Mem Size", 200],
          ["status", "Status", 200],
        ];
      case "machine_usage.csv":
        return [
          ["machine_id", "Machine ID", 200],
          ["time_stamp", "Time Stamp", 200],
          ["cpu_util_percent", "CPU Util Percent", 200],
          ["mem_util_percent", "Mem Util Percent", 200],
          ["mem_gps", "Mem GPS", 200],
          ["mpki", "MPKI", 200],
          ["net_in", "Net In", 200],
          ["net_out", "Net Out", 200],
          ["disk_io_percent", "Disk IO Percent", 200],
        ];
    }
  } else if (path[0].startsWith("microarchitecture")) {
    if (path[path.length - 1].startsWith("container_meta"))
      return [
        ["node_id", "Node ID", 200],
        ["container_id", "Container ID", 200],
        ["pod_id", "Pod ID", 200],
        ["cpu_mode", "CPU Mode", 200],
        ["app_name", "App Name", 200],
        ["deploy_group", "Deploy Group", 200],
        ["container_type", "Container Type", 200],
        ["container_cpu_spec", "Container CPU Spec", 200],
        ["container_mem_spec", "Container Mem Spec", 200],
        ["pod_cpu_spec", "Pod CPU Spec", 200],
        ["pod_mem_spec", "Pod Mem Spec", 200],
      ];
    else if (path[path.length - 1].startsWith("core_pmu"))
      return [
        ["ts", "Timestamp", 200],
        ["node_id", "Node ID", 200],
        ["container_id", "Container ID", 200],
        ["cpu", "CPU", 200],
        ["core_id", "Core ID", 200],
        ["socket_id", "Socket ID", 200],
        ["instructions", "Instructions", 200],
        ["cycles", "Cycles", 200],
        ["ref_cycles", "Ref Cycles", 200],
        ["llc_misses", "LLC Misses", 200],
      ];
    else if (path[path.length - 1].startsWith("uncore_pmu"))
      return [
        ["ts", "Timestamp", 200],
        ["node_id", "Node ID", 200],
        ["socket_id", "Socket ID", 200],
        ["channel_id", "Channel ID", 200],
        ["read_bw", "Read BW", 200],
        ["write_bw", "Write BW", 200],
        ["latency", "Latency", 200],
      ];
    else if (path[path.length - 1].startsWith("host_meta"))
      return [
        ["node_id", "Node ID", 200],
        ["cpu_num", "CPU Num", 200],
        ["machine_model", "Machine Model", 200],
        ["cpu_model", "CPU Model", 200],
        ["ref_freq_Ghz", "Ref Freq Ghz", 200],
        ["dimms_per_channel", "Dimms Per Channel", 200],
      ];
  } else if (path[0].startsWith("microservices")) {
    if (path[path.length - 1].startsWith("CallGraph"))
      return [
        ["timestamp", "Timestamp", 150],
        ["traceid", "Trace ID", 150],
        ["service", "Service", 200],
        ["rpc_id", "RPC ID", 200],
        ["um", "UM", 100],
        ["uminstanceid", "UM Instance ID", 200],
        ["rpctype", "RPC Type", 200],
        ["interface", "Interface", 200],
        ["dm", "DM", 200],
        ["dminstanceid", "DM Instance ID", 200],
        ["rt", "RT", 200],
      ];
    else if (path[path.length - 1].startsWith("MCRRTUpdate"))
      return [
        ["timestamp", "Timestamp", 200],
        ["msname", "MS Name", 200],
        ["msinstanceid", "MS Instance ID", 200],
        ["nodeid", "Node ID", 200],
        ["providerrpc_rt", "Provider RPC RT", 200],
        ["providerrpc_mcr", "Provider RPC MCR", 200],
        ["consumerrpc_rt", "Consumer RPC RT", 200],
        ["consumerrpc_mcr", "Consumer RPC MCR", 200],
        ["writemc_rt", "Write MC RT", 200],
        ["writemc_mcr", "Write MC MCR", 200],
        ["readmc_rt", "Read MC RT", 200],
        ["readmc_mcr", "Read MC MCR", 200],
        ["writedb_rt", "Write DB RT", 200],
        ["writedb_mcr", "Write DB MCR", 200],
        ["readdb_rt", "Read DB RT", 200],
        ["readdb_mcr", "Read DB MCR", 200],
        ["consumermq_rt", "Consumer MQ RT", 200],
        ["consumermq_mcr", "Consumer MQ MCR", 200],
        ["providermq_rt", "Provider MQ RT", 200],
        ["providermq_mcr", "Provider MQ MCR", 200],
        ["http_mcr", "HTTP MCR", 200],
        ["http_rt", "HTTP RT", 200],
      ];
    else if (path[path.length - 1].startsWith("MSMetricsUpdate"))
      return [
        ["timestamp", "Timestamp", 200],
        ["msname", "MS Name", 200],
        ["msinstanceid", "MS Instance ID", 200],
        ["nodeid", "Node ID", 200],
        ["cpu_utilization", "CPU Utilization", 200],
        ["memory_utilization", "Memory Utilization", 200],
      ];
    else if (path[path.length - 1].startsWith("NodeMetricsUpdate"))
      return [
        ["timestamp", "Timestamp", 200],
        ["nodeid", "Node ID", 200],
        ["cpu_utilization", "CPU Utilization", 200],
        ["memory_utilization", "Memory Utilization", 200],
      ];
  }
  return [{}];
};

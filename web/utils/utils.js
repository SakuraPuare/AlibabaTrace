export const getHeightWithoutHeader = () => {
  const header = document.querySelector("#header");
  return window.innerHeight - header.clientHeight;
};

export const getColumnDetails = (path) => {
  if (path[0].startsWith("trace"))
    switch (path[path.length - 1]) {
      case "batch_instance.csv":
        return [
          {
            key: "instance_name",
            dataKey: "instance_name",
            title: "Instance Name",
            width: 200,
          },
          {
            key: "task_name",
            dataKey: "task_name",
            title: "Task Name",
            width: 200,
          },
          {
            key: "job_name",
            dataKey: "job_name",
            title: "Job Name",
            width: 200,
          },
          {
            key: "task_type",
            dataKey: "task_type",
            title: "Task Type",
            width: 200,
          },
          {
            key: "status",
            dataKey: "status",
            title: "Status",
            width: 200,
          },
          {
            key: "start_time",
            dataKey: "start_time",
            title: "Start Time",
            width: 200,
          },
          {
            key: "end_time",
            dataKey: "end_time",
            title: "End Time",
            width: 200,
          },
          {
            key: "machine_id",
            dataKey: "machine_id",
            title: "Machine ID",
            width: 200,
          },
          {
            key: "seq_no",
            dataKey: "seq_no",
            title: "Seq No",
            width: 200,
          },
          {
            key: "total_seq_no",
            dataKey: "total_seq_no",
            title: "Total Seq No",
            width: 200,
          },
          {
            key: "cpu_avg",
            dataKey: "cpu_avg",
            title: "CPU Avg",
            width: 200,
          },
          {
            key: "cpu_max",
            dataKey: "cpu_max",
            title: "CPU Max",
            width: 200,
          },
          {
            key: "mem_avg",
            dataKey: "mem_avg",
            title: "Mem Avg",
            width: 200,
          },
          {
            key: "mem_max",
            dataKey: "mem_max",
            title: "Mem Max",
            width: 200,
          },
        ];
      case "batch_task.csv":
        return [
          {
            key: "task_name",
            dataKey: "task_name",
            title: "Task Name",
            width: 200,
          },
          {
            key: "instance_num",
            dataKey: "instance_num",
            title: "Instance Num",
            width: 200,
          },
          {
            key: "job_name",
            dataKey: "job_name",
            title: "Job Name",
            width: 200,
          },
          {
            key: "task_type",
            dataKey: "task_type",
            title: "Task Type",
            width: 200,
          },
          {
            key: "status",
            dataKey: "status",
            title: "Status",
            width: 200,
          },
          {
            key: "start_time",
            dataKey: "start_time",
            title: "Start Time",
            width: 200,
          },
          {
            key: "end_time",
            dataKey: "end_time",
            title: "End Time",
            width: 200,
          },
          {
            key: "plan_cpu",
            dataKey: "plan_cpu",
            title: "Plan CPU",
            width: 200,
          },
          {
            key: "plan_mem",
            dataKey: "plan_mem",
            title: "Plan Mem",
            width: 200,
          },
        ];
      case "container_meta.csv":
        return [
          {
            key: "container_id",
            dataKey: "container_id",
            title: "Container ID",
            width: 200,
          },
          {
            key: "machine_id",
            dataKey: "machine_id",
            title: "Machine ID",
            width: 200,
          },
          {
            key: "time_stamp",
            dataKey: "time_stamp",
            title: "Time Stamp",
            width: 200,
          },
          {
            key: "app_du",
            dataKey: "app_du",
            title: "App Du",
            width: 200,
          },
          {
            key: "status",
            dataKey: "status",
            title: "Status",
            width: 200,
          },
          {
            key: "cpu_request",
            dataKey: "cpu_request",
            title: "CPU Request",
            width: 200,
          },
          {
            key: "cpu_limit",
            dataKey: "cpu_limit",
            title: "CPU Limit",
            width: 200,
          },
          {
            key: "mem_size",
            dataKey: "mem_size",
            title: "Mem Size",
            width: 200,
          },
        ];
      case "container_usage.csv":
        return [
          {
            key: "container_id",
            dataKey: "container_id",
            title: "Container ID",
            width: 200,
          },
          {
            key: "machine_id",
            dataKey: "machine_id",
            title: "Machine ID",
            width: 200,
          },
          {
            key: "time_stamp",
            dataKey: "time_stamp",
            title: "Time Stamp",
            width: 200,
          },
          {
            key: "cpu_util_percent",
            dataKey: "cpu_util_percent",
            title: "CPU Util Percent",
            width: 200,
          },
          {
            key: "mem_util_percent",
            dataKey: "mem_util_percent",
            title: "Mem Util Percent",
            width: 200,
          },
          {
            key: "cpi",
            dataKey: "cpi",
            title: "CPI",
            width: 200,
          },
          {
            key: "mem_gps",
            dataKey: "mem_gps",
            title: "Mem GPS",
            width: 200,
          },
          {
            key: "mpki",
            dataKey: "mpki",
            title: "MPKI",
            width: 200,
          },
          {
            key: "net_in",
            dataKey: "net_in",
            title: "Net In",
            width: 200,
          },
          {
            key: "net_out",
            dataKey: "net_out",
            title: "Net Out",
            width: 200,
          },
          {
            key: "disk_io_percent",
            dataKey: "disk_io_percent",
            title: "Disk IO Percent",
            width: 200,
          },
        ];
      case "machine_meta.csv":
        return [
          {
            key: "machine_id",
            dataKey: "machine_id",
            title: "Machine ID",
            width: 200,
          },
          {
            key: "time_stamp",
            dataKey: "time_stamp",
            title: "Time Stamp",
            width: 200,
          },
          {
            key: "failure_domain_1",
            dataKey: "failure_domain_1",
            title: "Failure Domain 1",
            width: 200,
          },
          {
            key: "failure_domain_2",
            dataKey: "failure_domain_2",
            title: "Failure Domain 2",
            width: 200,
          },
          {
            key: "cpu_num",
            dataKey: "cpu_num",
            title: "CPU Num",
            width: 200,
          },
          {
            key: "mem_size",
            dataKey: "mem_size",
            title: "Mem Size",
            width: 200,
          },
          {
            key: "status",
            dataKey: "status",
            title: "Status",
            width: 200,
          },
        ];
      case "machine_usage.csv":
        return [
          {
            key: "machine_id",
            dataKey: "machine_id",
            title: "Machine ID",
            width: 200,
          },
          {
            key: "time_stamp",
            dataKey: "time_stamp",
            title: "Time Stamp",
            width: 200,
          },
          {
            key: "cpu_util_percent",
            dataKey: "cpu_util_percent",
            title: "CPU Util Percent",
            width: 200,
          },
          {
            key: "mem_util_percent",
            dataKey: "mem_util_percent",
            title: "Mem Util Percent",
            width: 200,
          },
          {
            key: "mem_gps",
            dataKey: "mem_gps",
            title: "Mem GPS",
            width: 200,
          },
          {
            key: "mpki",
            dataKey: "mpki",
            title: "MPKI",
            width: 200,
          },
          {
            key: "net_in",
            dataKey: "net_in",
            title: "Net In",
            width: 200,
          },
          {
            key: "net_out",
            dataKey: "net_out",
            title: "Net Out",
            width: 200,
          },
          {
            key: "disk_io_percent",
            dataKey: "disk_io_percent",
            title: "Disk IO Percent",
            width: 200,
          },
        ];
    }
  else if (path[0].startsWith("microservices"))
    return [
      {
        key: "timestamp",
        dataKey: "timestamp",
        title: "Timestamp",
        width: 200,
      },
      {
        key: "traceid",
        dataKey: "traceid",
        title: "Trace ID",
        width: 200,
      },
      {
        key: "service",
        dataKey: "service",
        title: "Service",
        width: 200,
      },
      {
        key: "rpc_id",
        dataKey: "rpc_id",
        title: "RPC ID",
        width: 200,
      },
      {
        key: "um",
        dataKey: "um",
        title: "UM",
        width: 200,
      },
      {
        key: "um_instance_id",
        dataKey: "um_instance_id",
        title: "UM Instance ID",
        width: 200,
      },
      {
        key: "rpc_type",
        dataKey: "rpc_type",
        title: "RPC Type",
        width: 200,
      },
      {
        key: "interface",
        dataKey: "interface",
        title: "Interface",
        width: 200,
      },
      {
        key: "dm",
        dataKey: "dm",
        title: "DM",
        width: 200,
      },
      {
        key: "dm_instance_id",
        dataKey: "dm_instance_id",
        title: "DM Instance ID",
        width: 200,
      },
      {
        key: "rt",
        dataKey: "rt",
        title: "RT",
        width: 200,
      },
    ];

  // if (path[path.length - 1].startsWith('core'))
  //   ;
  // else if (path[path.length - 1].startsWith('uncore'))
  //   ;
  return [];
};

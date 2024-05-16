<script setup></script>

<template>
  <div class="flex flex-col max-w-[60%] mx-auto space-y-6 mt-16">
    <h1 class="text-4xl">Alibaba Cluster Trace Program</h1>
    <h2 class="text-2xl">Overview</h2>
    <p>
      The Alibaba Cluster Trace Program is published by Alibaba Group. By
      providing cluster trace from real production, the program helps the
      researchers, students and people who are interested in the field to get
      better understanding of the characterastics of modern internet data
      centers (IDC's) and the workloads.
    </p>
    <p>So far, four versions of traces have been released:</p>
    <ul class="space-y-2 px-[2em] list-disc">
      <li>
        cluster-trace-v2017 includes about 1300 machines in a period of 12
        hours. The trace-v2017 firstly introduces the collocation of online
        services (aka long running applications) and batch workloads. To see
        more about this trace, see related documents (trace_2017). Download link
        is available after a short survey (survey link).
      </li>
      <li>
        cluster-trace-v2018 includes about 4000 machines in a period of 8 days.
        Besides having larger scaler than trace-v2017, this piece trace also
        contains the DAG information of our production batch workloads. See
        related documents for more details (trace_2018). Download link is
        available after a survey (less than a minute, survey link).
      </li>
      <li>
        cluster-trace-gpu-v2020 includes over 6500 GPUs (on ~1800 machines) in a
        period of 2 months. It describes the AI/ML workloads in the MLaaS
        (Machine-Learning-as-a-Service) provided by the Alibaba PAI (Platform
        for Artificial Intelligence) on GPU clusters. See the subdirectory
        (pai_gpu_trace_2020) for the released data, schema, and scripts for
        processing and visualization. Our analysis paper published in USENIX
        NSDI '22 is available here.
      </li>
      <li>
        cluster-trace-microservices-v2021 contains 20000+ microservices in a
        period of 12 hours. The traces the first released to introduce the
        runtime metrics of microservices in the production cluster, including
        call dependencies, respond time, call rates, and so on. See the
        subdirectory (trace_2021) for more details. Our analysis paper, accepted
        by SoCC '21, is available here.
      </li>
      <li>
        cluster-trace-microarchitecture-v2022 first provides AMTrace (Alibaba
        Microarchitecutre Trace). AMTrace is the first fine-granulairty and
        large-scale microarchitectural metrics of Alibaba Colocation Datacenter.
        Based AMTrace, researchers can analysis: CPU performance,
        microarchitecture contention, memory bandwidth contention and so on. Our
        paper is accepted by ICPP'22. See the subdirectory (trace_2022) for more
        details.
      </li>
      <li>
        cluster-trace-gpu-v2023 includes over 6200 GPUs (on ~1200 machines). It
        describes the AI/ML workloads with diverse resource specifications in a
        heterogeneous GPU cluster. In our "Beware of Fragmentation" paper
        (published in USENIX ATC '23), we modeled this trace in a Kubernetes
        Scheduler Simulator and demonstrated that our proposed Fragmentation
        Gradient Descent (FGD) policy outperforms classic scheduling policies
        like Best-Fit, Dot-Product, etc. See fgd_gpu_trace_2023 for the released
        data, schema, and scripts for processing.
      </li>
    </ul>
    <p>
      We encourage anyone to use the traces for study or research purposes, and
      if you had any question when using the trace, please contact us via email:
      alibaba-clusterdata, or file an issue on Github. Filing an issue is
      recommanded as the discussion would help all the community. Note that the
      more clearly you ask the question, the more likely you would get a clear
      answer.
    </p>
    <p>
      It would be much appreciated if you could tell us once any publication
      using our trace is available, as we are maintaining a list of related
      publicatioins for more researchers to better communicate with each other.
    </p>
    <p>
      In future, we will try to release new traces at a regular pace, please
      stay tuned.
    </p>
  </div>
</template>

<style scoped></style>

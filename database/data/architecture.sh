url='http://aliopentrace.oss-cn-beijing.aliyuncs.com/amtrace'
# mkdir database
# cd database

# mkdir container_meta_1k
# mkdir host_meta_1k
# mkdir core_pmu_1k
# mkdir uncore_pmu_1k
base_dir=$(pwd)

table_name="container_meta"
folder_name="${table_name}_1k"


for ((i = 0; i < 1; i++)); do
    command="${url}/${folder_name}/${table_name}-${i}.csv.gz"
    echo -e ${command}
done

table_name="host_meta"
folder_name="${table_name}_1k"


for ((i = 0; i < 1; i++)); do
    command="${url}/${folder_name}/${table_name}-${i}.csv.gz"
    echo -e ${command}
done

table_name="core_pmu"
folder_name="${table_name}_1k"


for ((i = 0; i < 108; i++)); do
    command="${url}/${folder_name}/${table_name}-${i}.csv.gz"
    echo -e ${command}
done

table_name="uncore_pmu"
folder_name="${table_name}_1k"


for ((i = 0; i < 20; i++)); do
    command="${url}/${folder_name}/${table_name}-${i}.csv.gz"
    echo -e ${command}
done
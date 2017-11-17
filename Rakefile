SERVICE = "distributed-cache"
IMAGE = "#{SERVICE}"

desc 'Run tests locally'
task :test_local do
  sh "nosetests -xw ./tests"
end

desc 'Build docker image'
task :build do
  sh "docker build -t #{IMAGE} ."
  puts "\n\Built: #{IMAGE}\n\n"
end

desc 'Launch cache nodes'
task :launch, [:num_machines] => [:build] do |t, args|
  # create network for docker containers
  sh "docker network create --subnet=172.19.0.0/16 distributed-cache-network || true"
  
  node_id = 0
  ip_prefix = "172.19.0.1"
  num_machines = args[:num_machines].to_i
  while node_id < num_machines do
      node_ip = ip_prefix + node_id.to_s
      linked_node_id = (node_id + 1) % num_machines
      linked_node_ip = ip_prefix + linked_node_id.to_s
      sh "docker run --net distributed-cache-network --ip #{node_ip} -e NODE_ID=#{node_id} -e NODE_IP=#{node_ip} -e LINKED_NODE_ID=#{linked_node_id} -e LINKED_NODE_IP=#{linked_node_ip} #{IMAGE} &"
      node_id += 1
  end
end

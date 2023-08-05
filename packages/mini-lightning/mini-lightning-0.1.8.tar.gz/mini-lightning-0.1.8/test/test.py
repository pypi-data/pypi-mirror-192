from libs import *
# 定义模型
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# 训练函数
def train(rank, world_size):
    # 初始化分布式环境
    dist.init_process_group('gloo', rank=rank, world_size=world_size)

    # 创建本地模型
    model = Net()

    # 使用DDP包装模型
    ddp_model = nn.parallel.DistributedDataParallel(model, device_ids=[rank])

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.01)

    # 模拟数据
    data = torch.randn(20, 10)
    target = torch.randn(20, 1)

    # 训练模型
    for epoch in range(10):
        # 每个epoch都需要手动设置一下种子，以避免每个进程采样的数据相同
        torch.manual_seed(epoch + rank)
        # 将数据划分到不同进程
        sampler = DistributedSampler(TensorDataset(data, target))
        loader = DataLoader(TensorDataset(data, target), batch_size=4, sampler=sampler)
        for i, (inputs, labels) in enumerate(loader):
            optimizer.zero_grad()
            print(inputs.device)
            outputs = ddp_model(inputs)
            print(outputs.device)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            if i % 10 == 0:
                print(f'Rank {rank}, Epoch {epoch}, Batch {i}, Loss {loss.item()}')

    # 清理分布式环境
    dist.destroy_process_group()

# 主函数
if __name__ == '__main__':
    # 启动两个进程
    spawn(train, args=(2,), nprocs=2, join=True)
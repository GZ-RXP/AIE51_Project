import threading

class BaseService(object):
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls is BaseService:
            raise TypeError("BaseService must be subclassed.")

        key = (cls, args, frozenset(kwargs.items()))

        if key not in cls._instances:
            with cls._lock:
                if key not in cls._instances:
                    # print(f"Creating new instance for: {key}")
                    instance = super(BaseService, cls).__new__(cls)
                    cls._instances[key] = instance
                # else:
                    # print(f"Another thread created the instance before acquiring the lock for: {key}")
        # else:
            # print(f"Returning existing instance for: {key}")

        return cls._instances[key]
    
# # 示例子类
# class MySingletonService(BaseService):
#     def __init__(self, value):
#         self.value = value
#         print(f"Initialized with value: {value}")

# # 测试代码
# if __name__ == "__main__":
#     # 创建两个具有相同参数的实例，应该返回同一个对象
#     s1 = MySingletonService(42)
#     s2 = MySingletonService(42)

#     # 创建另一个具有不同参数的实例，应该创建新的对象
#     s3 = MySingletonService(84)

#     print(s1 is s2)  # True
#     print(s1 is s3)  # False
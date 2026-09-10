class KernelError(Exception):
    """所有系统错误的爸爸（总类）"""
    pass


class PricingError(KernelError):
    """报价相关的错误"""
    pass


class MessageError(KernelError):
    """消息相关的错误"""
    pass


class RegistryError(KernelError):
    """注册表相关的错误"""
    pass

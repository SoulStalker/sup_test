import abc

from src.domain.registration.dtos import RegistrationDTO

from src.domain.user.entity import CreateUserEntity




class IRegistrationRepository(abc.ABC):
    
    @abc.abstractmethod
    def create(self, dto: CreateUserEntity):
        raise NotImplementedError

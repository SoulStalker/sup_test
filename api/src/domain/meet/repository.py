from src.models.meets import Category


class IMeetRepository:
    def create(self, meet):
        pass

    def delete(self, meet):
        pass

    def get_list(self, meet):
        pass


class ICategoryRepository:
    model = Category

    def create(self, category):
        pass

    def delete(self, category):
        pass

    def get_list(self) -> list[Category]:
        return Category.objects.all()

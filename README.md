# api_test

_test_add_pet_ - позитивный тест, создание объекта с минимальной структурой, тест проходит

_test_add_pet_existing_id_ - негатив. тест, создание объекта с уже существующим id. В тесте создаем объект с минимальной
структурой, сохраняем его id в перемененную. Отправляем еще один запрос на создание другого объекта с тем же id. Тест падает.

_test_add_pet_negative_id_ - негатив. тест, создание объекта в отрицательным id. Тест падает.

_test_add_pet_wrong_status_ - негатив. тест, создание объекта с несуществующим статусом. Тест падает.

_test_upload_image_ - позитив. тест, загрузка изображения для существующего объекта. Тест падает.

_test_update_pet_ - позитив. тест, обновление инфо о существующем объекте. Тест проходит.

_test_update_non_existent_pet_ - негатив. тест, обновление инфо о несуществующем объекте. Тест проходит.

_test_delete_pet_ - позитив. тест, удаление существующейго объекта. Тест проходит.

_test_delete_non_existent_pet_ - негатив. тест, удаление несуществующего объекта. Тест падает.

_test_delete_pet_without_api_key_ - негатив. тест, удаление объекта без соответствующего ключа в хедере. Тест падает.



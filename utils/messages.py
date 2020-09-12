def product_publish(name):
    text = "Здравствуйте! *Ваш товар '{}' ".format(name)
    text += "выставлен в каталог товаров,"
    text += "*Уведомления об аренде вашего товара и даты доставки Вы получите в"
    text += "*разделе 'Сообщения'. "
    text += "*Благодарим Вас за то, что Вы выбрали нашу платформу ALU.KZ! Мы рады, что"
    text += "*Вы являетесь нашим клиентом. "
    text += "*Если у Вас возникнут вопросы, пожалуйста, обращайтесь к нам."
    return text

def deliverthenpickup(name):
    text = "Здравствуйте!*" 
    text += "Ваш товар '{}' оформлен в заказе на аренду!*".format(name)
    text += "Вам необходимо выбрать удобную дату и время курьерской доставки для "
    text += "того чтобы забрать у вас товар. Курьерская служба - 400тг* или*"
    text += "Ждём Ваш выбор!*"
    return text

def pickUPoint(name):
    text = "Здравствуйте!*"
    text += "Ваш товар '{}' находится в пункте выдачи заказов.*".format(name)
    text += "Вам необходимо выбрать удобную дату и время курьерской доставки для*"
    text += "возврата товара. Курьерская служба - 400тг* или *"
    text += "*Если вы изъявите желание оставить ваш товар в нашем пункте выдачи*"
    text += "заказов, просим Вас нажать на нижнюю кнопку.*"
    text += "Ждём Ваш выбор!*"
    return text

def deliverOne(number, products, address, phone):
    text = "Здравствуйте!*"
    text += "Вами оформлен заказ №{}*".format(number)
    text += "Планируемый срок формирования заказа — от 1 до 3 дней*"
    text += "Уведомления обо всех изменениях заказа и даты комплектации товаров Вы*"
    text += "получите в разделе 'Сообщения'.**"

    text += "Заказанные товары:*"
    summ = 0
    for i in products:
        if i.count_day == 14:
            summ += i.price_14
            text += "'{}' - {} на 14 дней*".format(i.title, i.price_14)
        else:
            summ += i.price_30
            text += "'{}' - {} на 30 дней*".format(i.title, i.price_30)

    text += "**Метод доставки: Курьерская доставка*"
    text += "стоимость доставки: 800 тг.*"
    text += "Адрес доставки: {}**".format(address)

    text += "Итого: {} тг**".format(summ)

    text += "Контактный номер: {}**".format(phone)

    text += "Благодарим Вас за то, что Вы выбрали нашу платформу ALU.KZ! Мы рады, что*"
    text += "Вы являетесь нашим клиентом.*"
    text += "Если у Вас возникнут вопросы, пожалуйста, обращайтесь к нам.*"
    return text


def deliverTwo(number):
    text = "Здравствуйте!*"
    text += "Заказ №{} — сформирован и ожидает доставки.*".format(number)
    text += "Вам необходимо выбрать удобную дату и время курьерской доставки.*"
    text += "Ждём Ваш выбор!*"
    return text

def deliverThree(name):
    text = "Здравствуйте!"
    text += "До окончания вашей аренды на товар {} остался".format(name)
    text += "1 день.*"
    text += "Вам необходимо выбрать удобную дату и время курьерской доставки.*"
    text += "Ждём Ваш выбор!"
    return text


def PickupOne(number, products, phone):
    text = "Здравствуйте!*"
    text += "Вами оформлен заказ №{}*".format(number)
    text += "Планируемый срок формирования заказа — от 1 до 3 дней*"
    text += "Уведомления обо всех изменениях заказа и даты комплектации товаров Вы*"
    text += "получите в разделе 'Сообщения'.**"

    text += "Заказанные товары:*"
    summ = 0
    for i in products:
        if i.count_day == 14:
            summ += i.price_14
            text += "'{}' - {} на 14 дней*".format(i.title, i.price_14)
        else:
            summ += i.price_30
            text += "'{}' - {} на 30 дней*".format(i.title, i.price_30)

    text += "**Метод доставки: Пункт выдачи заказов*"
    text += "стоимость доставки: 0 тг.**"

    text += "Итого: {} тг**".format(summ)

    text += "Контактный номер: {}**".format(phone)

    text += "Благодарим Вас за то, что Вы выбрали нашу платформу ALU.KZ! Мы рады, что*"
    text += "Вы являетесь нашим клиентом.*"
    text += "Если у Вас возникнут вопросы, пожалуйста, обращайтесь к нам.*"
    return text

def PickupTwo(number):
    text = "Здравствуйте!*"
    text += "Заказ №{} — готов и находится в пункте выдачи заказов.*".format(number)
    text += "Мы ждем Вас по адресу:*"
    text += "Режим работы: Ежедневно с 10:00 до19:00*"
    text += "Просим Вас получить заказ в течение 3 дней.*"
    text += "Всего Вам доброго!"
    return text

def PickupThree(name):
    text = "Здравствуйте!*"
    text += "До окончания вашей аренды на товар {} остался 1 день.*".format(name)
    text += "Просим Вас возвратить заказ в течение 2 дней.*"
    text += "Мы ждем Вас по адресу:*"
    text += "Режим работы: Ежедневно с 10:00 до19:00*"
    text += "Всего Вам доброго!*"
    return text
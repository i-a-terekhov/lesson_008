from termcolor import cprint
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    total_food = 0
    max_dirty = 0

    def __init__(self):
        self.name = 'Дом'
        self.money = 100
        self.food = 50
        self.dirty = 0
        self.food_for_cat = 30
        self.cat_is_alive = True

    def act(self):
        self.dirty += 5
        if self.dirty > self.max_dirty:
            self.max_dirty = self.dirty

    def food_is_end(self):
        cprint('В доме заканчивается еда!', color='red')
        if self.food < 30:
            return True
        else:
            return False

    def money_is_end(self):
        if self.money == 0:
            return True
        else:
            return False

    def food_for_cat_is_end(self):
        cprint('В доме заканчивается китикет', color='red')
        if self.food_for_cat < 20:
            return True
        else:
            return False

    def __str__(self):
        return 'В доме есть {} ед. денег, и {} ед. еды и {} ед. китекета. Уровень грязи равен {}'.format(
            self.money, self.food, self.food_for_cat, self.dirty)


class Human:

    total_dirty_time = 0
    total_petting_cat = 0

    def __init__(self, name, house):
        self.name = name
        self.satiety = 30  # сытость
        self.happiness = 100
        self.house = house
        self.there_was_no_action = True

    def __str__(self):
        return 'Персонаж {} живет в доме {}, сыт на {}, счастлив на {}'.format(
            self.name, self.house.name, self.satiety, self.happiness)

    def act(self):
        self.satiety -= 10
        if self.house.dirty > 100:
            self.happiness -= 5
            self.total_dirty_time += 1

        print('Персонаж {} выбирает что делать...'.format(self.name))
        self.there_was_no_action = True

        if self.satiety < 50:
            print('Персонаж {} захотел покушать'.format(self.name))
            self.eat()

        elif randint(1, 10) > 8:
            print('Персонаж {} решил погладить кота'.format(self.name))
            self.petting_cat()
            self.total_petting_cat += 1
            self.there_was_no_action = False

    def eat(self):
        if self.house.food == 0:
            print('Покушать не удалось, т.к. вся еда закончилась...')
            self.there_was_no_action = True
        else:
            volume_of_food = 40
            if volume_of_food > self.house.food > 0:
                volume_of_food = self.house.food
            self.satiety += volume_of_food + 10  # условие задания +10 из-за затрат 10 ед. на любое действие
            self.there_was_no_action = False
            self.house.food -= volume_of_food
            print('Персонаж {} покушал на {} ед. еды, осталось еды {}'.format(
                self.name, volume_of_food, self.house.food))

    def is_not_death(self):
        if self.satiety >= 0 and self.happiness >= 10:
            return True
        elif self.satiety < 0:
            print('Персонаж {} умер от голода'.format(self.name))
            return False
        elif self.happiness < 10:
            print('Персонаж {} умер от депрессии'.format(self.name))
            return False

    def petting_cat(self):
        if self.house.cat_is_alive:
            self.happiness += 5
        else:
            print('Котик мертв... Счастье понижается')
            self.happiness -= 15


class Husband(Human):

    total_earned = 0  # всего заработано

    def act(self):
        super().act()
        if self.there_was_no_action:
            if self.house.money_is_end():
                cprint('В доме закончились все деньги!', color='red')
                self.work()
            elif self.happiness < 50:
                print('Персонаж {} решил поиграть в танки'.format(self.name))
                self.gaming()
            else:
                print('Персонаж {} от безысходности решил поработать'.format(self.name))
                self.happiness -= 5
                self.work()

    def work(self):
        self.house.money += 150
        self.total_earned += 150
        print('Персонаж {} пошел на работу. Теперь денег в доме стало {}'.format(self.name, self.house.money))
        pass

    def gaming(self):
        self.happiness += 20
        if self.happiness > 100:
            self.happiness = 100


class Wife(Human):

    total_coat_buy = 0

    def act(self):
        super().act()
        if self.there_was_no_action:
            if self.house.food_is_end() or self.house.food_for_cat_is_end():
                self.shopping()
            elif self.house.dirty > 30:
                print('Персонаж {} решил убраться в доме'.format(self.name))
                self.clean_house()
            elif self.house.money > 350 and (self.happiness < 50 or randint(1, 10) > 9):
                print('Персонаж {} решил купить дорогущую шубу'.format(self.name))
                self.buy_fur_coat()
            else:
                print('Персонаж {} не нашел для себя занятия, уровень счастья понизился...'.format(self.name))
                self.happiness -= 5

    def shopping(self):
        if self.house.money == 0:
            print('Персонаж {} хочет сходить за продуктами, но денег нет'.format(self.name))
            return
        volume_of_products = 120
        if volume_of_products > self.house.money:
            volume_of_products = self.house.money

        cat_food = int(volume_of_products / 4)
        human_food = volume_of_products - cat_food

        self.house.money -= volume_of_products
        self.house.food += human_food
        self.house.food_for_cat += cat_food
        self.house.total_food += human_food
        print('Персонаж {} купил {} ед. продуктов и {} ед. котиковой еды'.format(self.name, human_food, cat_food))

    def buy_fur_coat(self):
        self.house.money -= 350
        self.happiness += 60
        if self.happiness > 100:
            self.happiness = 100
        self.total_coat_buy += 1

    def clean_house(self):
        volume_of_clean = 150
        if self.house.dirty < volume_of_clean:
            volume_of_clean = self.house.dirty
        self.house.dirty -= volume_of_clean


class Cat:

    def __init__(self, name, house):
        self.name = name
        self.house = house
        self.satiety = 30  # сытость
        self.house.cat_is_alive = True

    def __str__(self):
        return 'Котик {} живет в доме {}, сыт на {}'.format(
            self.name, self.house.name, self.satiety)

    def act(self):
        self.satiety -= 5
        if self.satiety < 30:
            print('Кот {} решает покушать'.format(self.name))
            self.eat()
        elif randint(1, 10) > 7:
            print('Котик {} решает подрать обои'.format(self.name))
            self.tear_up_the_wallpaper()
        else:
            print('Котик {} решает поспать'.format(self.name))
            self.sleep()

    def eat(self):
        if self.house.food_for_cat == 0:
            cprint('В доме закончилась котиковная еда!', color='red')
        else:
            volume_of_cat_food = 5 + 10 * randint(0, 10)
            if self.house.food_for_cat < volume_of_cat_food:
                volume_of_cat_food = self.house.food_for_cat
            self.satiety += (volume_of_cat_food * 2) + 10  # условие задания +10 из-за затрат 10 ед. на любое действие
            self.house.food_for_cat -= volume_of_cat_food
            print('Кот {} покушал на {} ед.'.format(self.name, volume_of_cat_food))

    def sleep(self):
        print('Котик {} сладенько спит'.format(self.name))

    def tear_up_the_wallpaper(self):
        self.house.dirty += 15

    def is_not_death(self):
        if self.satiety >= 0:
            self.house.cat_is_alive = True
            return True
        elif self.satiety < 0:
            print('Персонаж {} умер от голода'.format(self.name))
            self.house.cat_is_alive = False
            return False


class Child(Human):

    def __init__(self, name, house):
        super().__init__(name=name, house=house)

    def __str__(self):
        return super().__str__()

    def act(self):
        self.satiety -= 5

        print('Персонаж {} выбирает что делать...'.format(self.name))
        if self.satiety < 70:
            print('Персонаж {} захотел покушать'.format(self.name))
            if self.house.food_is_end():
                cprint('В доме закончилась еда!', color='red')
            else:
                self.eat()
        else:
            print('Персонаж {} захотел поспать'.format(self.name))
            self.sleep()

    def eat(self):
        volume_of_food = 10
        if 10 > self.house.food > 0:
            volume_of_food = self.house.food
        self.satiety += volume_of_food + 5  # условие задания +5 из-за затрат 10 ед. на любое действие
        self.house.food -= volume_of_food
        print('Персонаж {} покушал на {} ед. еды, осталось еды {}'.format(self.name, volume_of_food, self.house.food))

    def sleep(self):
        print('Персонаж {} сладенько спит'.format(self.name))


home = House()
serge = Husband(name='Сережа', house=home)
masha = Wife(name='Маша', house=home)
spinogriz = Child(name='Спиногрыз', house=home)
bubble = Cat(name='Бубл', house=home)
dubble = Cat(name='Дубл', house=home)
hubble = Cat(name='Хубл', house=home)
family = [
    serge,
    masha,
    spinogriz,
    bubble,
    dubble,
    hubble,
    home,
]

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')

    # заставляем действовать каждый элемент семьи:
    for each in family:
        if hasattr(each, 'is_not_death'):
            if each.is_not_death():
                each.act()
            else:
                family.remove(each)
        else:
            each.act()

    # выводим __str__ каждого элемента семьи:
    for each in family:
        if hasattr(each, 'is_not_death'):
            if each.is_not_death():
                cprint(str(each), color='cyan')
            else:
                family.remove(each)
        else:
            cprint(str(each), color='cyan')


print('ИТОГО заработано: {}'.format(serge.total_earned))
print('ИТОГО шуб куплено: {}'.format(masha.total_coat_buy))
print('ИТОГО продуктов куплено: {}'.format(home.total_food))
print('ИТОГО дней срача: {}'.format(serge.total_dirty_time))
print('Максимальный срач: {}'.format(home.max_dirty))
print('ИТОГО погладили кота: {}'.format(serge.total_petting_cat))
print('ИТОГО погладили кота: {}'.format(masha.total_petting_cat))



######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

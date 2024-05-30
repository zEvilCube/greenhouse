MESSAGE_GREETING = "👋Привет, {}!"
MESSAGE_HELP = "/auth - сменить теплицу\n/menu - главное меню\n/reference - изменить эталонный показатель"
MESSAGE_INPUT_INVALID = "❌ Ошибка ввода."
MESSAGE_INPUT_SUCCESS = "✅ Ввод принят."

BUTTON_BACK = "⬅️ Назад"
BUTTON_REFRESH = "🔄 Обновить"

COMMAND_AUTH = "auth"
BUTTON_AUTH = "🌿 Сменить теплицу"
MESSAGE_AUTH_PENDING = "💬 Пожалуйста, введите api-ключ теплицы:"
MESSAGE_AUTH_INVALID = "❌ Неверный api-ключ. Попробуйте ещё раз:"

COMMAND_MENU = "menu"
MESSAGE_GREENHOUSE = "Статус теплицы №{}:\n\nТекущие показатели:\n{}\n\nСтатусы контроллеров:\n{}"
MESSAGE_SENSOR = "{}. {}: {} / {}"
MESSAGE_CONTROLLER = "{}. {}: {}"

COMMAND_REFERENCE = "reference"
BUTTON_REFERENCE = "🌡️ Изменить эталон"
MESSAGE_REFERENCE_CHOOSING = "🎹 Выберите датчик:"
MESSAGE_REFERENCE_PENDING = "💬 Введите новое эталонное значение:"
MESSAGE_REFERENCE_INVALID_SENSOR = "❌ Неверный id сенсора."
BUTTON_REFERENCE_SENSOR = "{} {}"

EMOJIS_SENSORS = {
    "LIGHT": "💡",
    "TEMPERATURE": "🌡️",
    "COOLING": "❄️",
    "HEATING": "🔥",
    "HUMIDITY": "💧"
}

EMOJIS_STATUSES = {
    False: "⚪",
    True: "🟢",
    None: "⚪"
}

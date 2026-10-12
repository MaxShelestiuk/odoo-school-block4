# hr_hospital — практичне завдання блоку 4 для Odoo 19

Репозиторій містить навчальний модуль `hr_hospital`, продовжений після блоків 2 і 3. Модуль розміщений у каталозі `hr_hospital/`, тому його технічна назва не залежить від назви каталогу клонованого репозиторію.

## Реалізовано

- повна форма візиту зі statusbar, stat button, chatter і всіма полями;
- list із searchpanel за лікарем та ієрархічною хворобою;
- calendar, pivot за лікарями/статусами/місяцями та stacked graph за хворобами;
- шість додаткових демо-візитів у різних місяцях;
- форма пацієнта з історією візитів, швидким записом і пошуком за ПІБ або телефоном;
- форма лікаря з ментором та вбудованим kanban інтернів;
- kanban лікарів із трьома кваліфікаційними колонками, швидким записом і меню картки;
- фільтри «Ментори», «Інтерни» та два нові демо-інтерни;
- ієрархічний searchpanel захворювань із фільтрацією нащадків;
- візард звіту за лікарями, хворобами й періодом у системному меню Print лікаря;
- серверна дія для виділених протермінованих візитів і щоденний `ir.cron`;
- адресний tracking статусу й лікаря через `mail.thread`;
- автоматичні тести вимог блоку 4.

Швидке створення візиту реалізоване `type="object"`-кнопками. Python-метод повертає модальну форму з `default_patient_id` або `default_doctor_id` у context. XML-коментар із поясненням рішення є у формі пацієнта.

## Структура

```text
hr_hospital/
├── data/       # майстер-дані, серверна дія, cron
├── demo/       # лікарі, інтерни, пацієнти, хвороби, візити
├── models/     # моделі та бізнес-логіка
├── security/   # ACL
├── tests/      # автоматичні тести блоків
├── views/      # list, form, search, kanban, calendar, pivot, graph
└── wizard/     # звітні та масові візарди
```

## Перевірка

Команди запускаються з кореня репозиторію. Шляхи відповідають локальному навчальному середовищу.

```bash
/home/max-shelestiuk/odoo_dev/venv/bin/ruff check hr_hospital scripts

/home/max-shelestiuk/odoo_dev/venv/bin/python \
  /home/max-shelestiuk/odoo_dev/odoo/odoo-bin \
  -c /home/max-shelestiuk/odoo_dev/config/odoo.conf \
  -d odoo_block4_dev -u hr_hospital \
  --test-enable --test-tags /hr_hospital \
  --stop-after-init --http-interface=127.0.0.1
```

Чисте встановлення без демоданих:

```bash
/home/max-shelestiuk/odoo_dev/venv/bin/python \
  /home/max-shelestiuk/odoo_dev/odoo/odoo-bin \
  -c /home/max-shelestiuk/odoo_dev/config/odoo.conf \
  -d odoo_block4_clean -i hr_hospital --without-demo=True \
  --stop-after-init --http-interface=127.0.0.1
```

Детальні результати автоматичної й браузерної перевірки наведені у [VERIFICATION.md](VERIFICATION.md).

## Git-процес

Гілка репозиторію — `19.0`. Репозиторій створений незалежним локальним клоном блоку 3 зі збереженням повної історії. Кожний завершений етап оформлений окремим локальним комітом. Remote попереднього блоку видалено; push на GitHub не виконувався.

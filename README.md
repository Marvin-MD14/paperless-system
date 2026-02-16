
```
paperless-system
├─ manage.py
├─ paperless_site
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ __init__.py
├─ requirements.txt
├─ static
│  └─ assets
│     ├─ .babelrc
│     ├─ css
│     │  ├─ admin_style.css
│     │  └─ style.css
│     ├─ favicon.ico
│     ├─ gulpfile.js
│     ├─ images
│     │  └─ capitol.png
│     ├─ img
│     │  ├─ bg1.jpg
│     │  ├─ bg10.jpg
│     │  ├─ bg2.jpg
│     │  ├─ bg3.jpg
│     │  ├─ bg4.jpg
│     │  ├─ bg5.jpg
│     │  ├─ bg6.jpg
│     │  ├─ bg7.jpg
│     │  ├─ bg8.jpg
│     │  ├─ bg9.jpg
│     │  ├─ capitol_logo.png
│     │  ├─ dummy.png
│     │  ├─ lock-bg.jpg
│     │  ├─ logo-single.png
│     │  ├─ logo.png
│     │  ├─ mb-sample.jpg
│     │  ├─ mockup.png
│     │  ├─ profile-bg.jpg
│     │  └─ user
│     │     ├─ 01.jpg
│     │     ├─ 02.jpg
│     │     ├─ 03.jpg
│     │     ├─ 04.jpg
│     │     ├─ 05.jpg
│     │     ├─ 06.jpg
│     │     ├─ 07.jpg
│     │     ├─ 08.jpg
│     │     ├─ 09.jpg
│     │     ├─ 10.jpg
│     │     ├─ 11.jpg
│     │     ├─ 12.jpg
│     │     └─ 13.jpg
│     ├─ js
│     │  ├─ app.init.js
│     │  ├─ custom
│     │  │  └─ custom.js
│     │  ├─ index.js
│     │  └─ modules
│     │     ├─ charts
│     │     │  ├─ chart-knob.js
│     │     │  ├─ chart.js
│     │     │  ├─ chartist.js
│     │     │  ├─ easypiechart.js
│     │     │  ├─ flot.js
│     │     │  ├─ morris.js
│     │     │  ├─ rickshaw.js
│     │     │  └─ sparkline.js
│     │     ├─ common
│     │     │  ├─ bootstrap-start.js
│     │     │  ├─ card-tools.js
│     │     │  ├─ constants.js
│     │     │  ├─ fullscreen.js
│     │     │  ├─ load-css.js
│     │     │  ├─ localize.js
│     │     │  ├─ navbar-search.js
│     │     │  ├─ now.js
│     │     │  ├─ rtl.js
│     │     │  ├─ sidebar.js
│     │     │  ├─ slimscroll.js
│     │     │  ├─ table-checkall.js
│     │     │  ├─ toggle-state.js
│     │     │  ├─ trigger-resize.js
│     │     │  └─ wrapper.js
│     │     ├─ elements
│     │     │  ├─ cards.js
│     │     │  ├─ nestable.js
│     │     │  ├─ notify.js
│     │     │  ├─ porlets.js
│     │     │  ├─ sortable.js
│     │     │  └─ sweetalert.js
│     │     ├─ extras
│     │     │  ├─ calendar.js
│     │     │  ├─ jqcloud.js
│     │     │  └─ search.js
│     │     ├─ forms
│     │     │  ├─ color-picker.js
│     │     │  ├─ forms.js
│     │     │  ├─ imagecrop.js
│     │     │  ├─ select2.js
│     │     │  ├─ upload.js
│     │     │  ├─ wizard.js
│     │     │  └─ xeditable.js
│     │     ├─ maps
│     │     │  ├─ gmap.js
│     │     │  ├─ vector.map.demo.js
│     │     │  └─ vector.map.js
│     │     ├─ pages
│     │     │  └─ pages.js
│     │     └─ tables
│     │        ├─ bootgrid.js
│     │        └─ datatable.js
│     ├─ modernizr-config.json
│     ├─ package-lock.json
│     ├─ package.json
│     ├─ pug
│     │  ├─ views
│     │  │  ├─ charts
│     │  │  │  ├─ chart-chartist.pug
│     │  │  │  ├─ chart-flot.pug
│     │  │  │  ├─ chart-js.pug
│     │  │  │  ├─ chart-morris.pug
│     │  │  │  ├─ chart-radial.pug
│     │  │  │  └─ chart-rickshaw.pug
│     │  │  ├─ dashboard
│     │  │  │  ├─ dashboard.pug
│     │  │  │  ├─ dashboard_h.pug
│     │  │  │  ├─ dashboard_v2.pug
│     │  │  │  └─ dashboard_v3.pug
│     │  │  ├─ elements
│     │  │  │  ├─ buttons.pug
│     │  │  │  ├─ cards.pug
│     │  │  │  ├─ carousel.pug
│     │  │  │  ├─ colors.pug
│     │  │  │  ├─ dropdown-animations.pug
│     │  │  │  ├─ grid-masonry.pug
│     │  │  │  ├─ grid.pug
│     │  │  │  ├─ icons-font.pug
│     │  │  │  ├─ icons-weather.pug
│     │  │  │  ├─ nestable.pug
│     │  │  │  ├─ notifications.pug
│     │  │  │  ├─ portlets.pug
│     │  │  │  ├─ sortable.pug
│     │  │  │  ├─ spinners.pug
│     │  │  │  ├─ sweetalert.pug
│     │  │  │  ├─ template.pug
│     │  │  │  └─ typo.pug
│     │  │  ├─ extras
│     │  │  │  ├─ blog-article-view.pug
│     │  │  │  ├─ blog-articles.pug
│     │  │  │  ├─ blog-post.pug
│     │  │  │  ├─ blog.pug
│     │  │  │  ├─ bug-tracker.pug
│     │  │  │  ├─ calendar.pug
│     │  │  │  ├─ contact-details.pug
│     │  │  │  ├─ contacts.pug
│     │  │  │  ├─ ecommerce-checkout.pug
│     │  │  │  ├─ ecommerce-order-view.pug
│     │  │  │  ├─ ecommerce-orders.pug
│     │  │  │  ├─ ecommerce-product-view.pug
│     │  │  │  ├─ ecommerce-products.pug
│     │  │  │  ├─ faq.pug
│     │  │  │  ├─ file-manager.pug
│     │  │  │  ├─ followers.pug
│     │  │  │  ├─ forum-categories.pug
│     │  │  │  ├─ forum-discussion.pug
│     │  │  │  ├─ forum-topics.pug
│     │  │  │  ├─ help-center.pug
│     │  │  │  ├─ invoice.pug
│     │  │  │  ├─ mailbox.pug
│     │  │  │  ├─ plans.pug
│     │  │  │  ├─ profile.pug
│     │  │  │  ├─ project-details.pug
│     │  │  │  ├─ projects.pug
│     │  │  │  ├─ search.pug
│     │  │  │  ├─ settings.pug
│     │  │  │  ├─ social-board.pug
│     │  │  │  ├─ team-viewer.pug
│     │  │  │  ├─ timeline.pug
│     │  │  │  ├─ todo.pug
│     │  │  │  └─ vote-links.pug
│     │  │  ├─ forms
│     │  │  │  ├─ form-extended.pug
│     │  │  │  ├─ form-imagecrop.pug
│     │  │  │  ├─ form-standard.pug
│     │  │  │  ├─ form-upload.pug
│     │  │  │  ├─ form-validation.pug
│     │  │  │  ├─ form-wizard.pug
│     │  │  │  └─ form-xeditable.pug
│     │  │  ├─ maps
│     │  │  │  ├─ maps-google.pug
│     │  │  │  └─ maps-vector.pug
│     │  │  ├─ multilevel
│     │  │  │  ├─ multilevel-1.pug
│     │  │  │  └─ multilevel-3.pug
│     │  │  ├─ pages
│     │  │  │  ├─ 404.pug
│     │  │  │  ├─ 500.pug
│     │  │  │  ├─ lock.pug
│     │  │  │  ├─ login.pug
│     │  │  │  ├─ maintenance.pug
│     │  │  │  ├─ recover.pug
│     │  │  │  └─ register.pug
│     │  │  ├─ tables
│     │  │  │  ├─ table-bootgrid.pug
│     │  │  │  ├─ table-datatable.pug
│     │  │  │  ├─ table-extended.pug
│     │  │  │  └─ table-standard.pug
│     │  │  ├─ widgets
│     │  │  │  └─ widgets.pug
│     │  │  └─ _partials
│     │  │     ├─ _chat.pug
│     │  │     ├─ _footer.pug
│     │  │     ├─ _footer_page.pug
│     │  │     ├─ _head.pug
│     │  │     ├─ _offsidebar.pug
│     │  │     ├─ _scripts.pug
│     │  │     ├─ _settings.pug
│     │  │     ├─ _sidebar.pug
│     │  │     ├─ _top-navbar.pug
│     │  │     └─ _top-navbar_h.pug
│     │  ├─ _layout.pug
│     │  ├─ _layout_h.pug
│     │  └─ _layout_page.pug
│     ├─ sass
│     │  ├─ app
│     │  │  ├─ charts
│     │  │  │  ├─ chart-easypie.scss
│     │  │  │  ├─ chart-flot.scss
│     │  │  │  └─ radial-bar.scss
│     │  │  ├─ common
│     │  │  │  ├─ animate.scss
│     │  │  │  ├─ bootstrap-custom.scss
│     │  │  │  ├─ bootstrap-reset.scss
│     │  │  │  ├─ button-extra.scss
│     │  │  │  ├─ cards.scss
│     │  │  │  ├─ circles.scss
│     │  │  │  ├─ dropdown-extra.scss
│     │  │  │  ├─ half-float.scss
│     │  │  │  ├─ inputs.scss
│     │  │  │  ├─ placeholder.scss
│     │  │  │  ├─ print.scss
│     │  │  │  ├─ slim-scroll.scss
│     │  │  │  ├─ typo.scss
│     │  │  │  ├─ utils.scss
│     │  │  │  └─ variables.scss
│     │  │  ├─ elements
│     │  │  │  ├─ nestable.scss
│     │  │  │  ├─ notify.scss
│     │  │  │  ├─ portlets.scss
│     │  │  │  └─ spinner.scss
│     │  │  ├─ extras
│     │  │  │  ├─ calendar.scss
│     │  │  │  ├─ mailbox.scss
│     │  │  │  ├─ plans.scss
│     │  │  │  ├─ timeline.scss
│     │  │  │  └─ todo.scss
│     │  │  ├─ forms
│     │  │  │  ├─ dropzone.scss
│     │  │  │  ├─ form-datepicker.scss
│     │  │  │  ├─ form-imgcrop.scss
│     │  │  │  ├─ form-tags.scss
│     │  │  │  ├─ form-validation.scss
│     │  │  │  ├─ form-wizard.scss
│     │  │  │  └─ plugins.scss
│     │  │  ├─ layout
│     │  │  │  ├─ layout-animation.scss
│     │  │  │  ├─ layout-extra.scss
│     │  │  │  ├─ layout.scss
│     │  │  │  ├─ offsidebar.scss
│     │  │  │  ├─ settings.scss
│     │  │  │  ├─ sidebar.scss
│     │  │  │  ├─ top-navbar.scss
│     │  │  │  └─ user-block.scss
│     │  │  ├─ maps
│     │  │  │  ├─ gmap.scss
│     │  │  │  └─ vector-map.scss
│     │  │  └─ tables
│     │  │     ├─ bootgrid.scss
│     │  │     ├─ datatable.scss
│     │  │     └─ table-extras.scss
│     │  ├─ app.scss
│     │  ├─ bootstrap
│     │  │  ├─ bootstrap-grid.scss
│     │  │  ├─ bootstrap-reboot.scss
│     │  │  ├─ bootstrap.scss
│     │  │  ├─ mixins
│     │  │  │  ├─ _alert.scss
│     │  │  │  ├─ _background-variant.scss
│     │  │  │  ├─ _badge.scss
│     │  │  │  ├─ _border-radius.scss
│     │  │  │  ├─ _box-shadow.scss
│     │  │  │  ├─ _breakpoints.scss
│     │  │  │  ├─ _buttons.scss
│     │  │  │  ├─ _caret.scss
│     │  │  │  ├─ _clearfix.scss
│     │  │  │  ├─ _deprecate.scss
│     │  │  │  ├─ _float.scss
│     │  │  │  ├─ _forms.scss
│     │  │  │  ├─ _gradients.scss
│     │  │  │  ├─ _grid-framework.scss
│     │  │  │  ├─ _grid.scss
│     │  │  │  ├─ _hover.scss
│     │  │  │  ├─ _image.scss
│     │  │  │  ├─ _list-group.scss
│     │  │  │  ├─ _lists.scss
│     │  │  │  ├─ _nav-divider.scss
│     │  │  │  ├─ _pagination.scss
│     │  │  │  ├─ _reset-text.scss
│     │  │  │  ├─ _resize.scss
│     │  │  │  ├─ _screen-reader.scss
│     │  │  │  ├─ _size.scss
│     │  │  │  ├─ _table-row.scss
│     │  │  │  ├─ _text-emphasis.scss
│     │  │  │  ├─ _text-hide.scss
│     │  │  │  ├─ _text-truncate.scss
│     │  │  │  ├─ _transition.scss
│     │  │  │  └─ _visibility.scss
│     │  │  ├─ utilities
│     │  │  │  ├─ _align.scss
│     │  │  │  ├─ _background.scss
│     │  │  │  ├─ _borders.scss
│     │  │  │  ├─ _clearfix.scss
│     │  │  │  ├─ _display.scss
│     │  │  │  ├─ _embed.scss
│     │  │  │  ├─ _flex.scss
│     │  │  │  ├─ _float.scss
│     │  │  │  ├─ _interactions.scss
│     │  │  │  ├─ _overflow.scss
│     │  │  │  ├─ _position.scss
│     │  │  │  ├─ _screenreaders.scss
│     │  │  │  ├─ _shadows.scss
│     │  │  │  ├─ _sizing.scss
│     │  │  │  ├─ _spacing.scss
│     │  │  │  ├─ _stretched-link.scss
│     │  │  │  ├─ _text.scss
│     │  │  │  └─ _visibility.scss
│     │  │  ├─ vendor
│     │  │  │  └─ _rfs.scss
│     │  │  ├─ _alert.scss
│     │  │  ├─ _badge.scss
│     │  │  ├─ _breadcrumb.scss
│     │  │  ├─ _button-group.scss
│     │  │  ├─ _buttons.scss
│     │  │  ├─ _card.scss
│     │  │  ├─ _carousel.scss
│     │  │  ├─ _close.scss
│     │  │  ├─ _code.scss
│     │  │  ├─ _custom-forms.scss
│     │  │  ├─ _dropdown.scss
│     │  │  ├─ _forms.scss
│     │  │  ├─ _functions.scss
│     │  │  ├─ _grid.scss
│     │  │  ├─ _images.scss
│     │  │  ├─ _input-group.scss
│     │  │  ├─ _jumbotron.scss
│     │  │  ├─ _list-group.scss
│     │  │  ├─ _media.scss
│     │  │  ├─ _mixins.scss
│     │  │  ├─ _modal.scss
│     │  │  ├─ _nav.scss
│     │  │  ├─ _navbar.scss
│     │  │  ├─ _pagination.scss
│     │  │  ├─ _popover.scss
│     │  │  ├─ _print.scss
│     │  │  ├─ _progress.scss
│     │  │  ├─ _reboot.scss
│     │  │  ├─ _root.scss
│     │  │  ├─ _spinners.scss
│     │  │  ├─ _tables.scss
│     │  │  ├─ _toasts.scss
│     │  │  ├─ _tooltip.scss
│     │  │  ├─ _transitions.scss
│     │  │  ├─ _type.scss
│     │  │  ├─ _utilities.scss
│     │  │  └─ _variables.scss
│     │  ├─ bootstrap.scss
│     │  └─ themes
│     │     ├─ theme-a.scss
│     │     ├─ theme-b.scss
│     │     ├─ theme-c.scss
│     │     ├─ theme-d.scss
│     │     ├─ theme-e.scss
│     │     ├─ theme-f.scss
│     │     ├─ theme-g.scss
│     │     └─ theme-h.scss
│     ├─ server
│     │  ├─ datatable.json
│     │  ├─ i18n
│     │  │  ├─ site-en.json
│     │  │  └─ site-es.json
│     │  └─ xeditable-groups.json
│     ├─ sidebar.json
│     └─ vendor.json
├─ templates
│  ├─ admin_dashboard.html
│  ├─ admin_login.html
│  ├─ base.html
│  ├─ dashboard.html
│  ├─ head_dashboard.html
│  ├─ head_login.html
│  ├─ includes
│  │  ├─ admin_sidebar.html
│  │  ├─ employee_sidebar.html
│  │  ├─ governor_sidebar.html
│  │  └─ head_sidebar.html
│  ├─ login.html
│  └─ register.html
└─ tracking
   ├─ admin.py
   ├─ apps.py
   ├─ migration
   │  └─ __init__.py
   ├─ migrations
   │  ├─ 0001_initial.py
   │  ├─ 0002_alter_department_id_alter_userprofile_id.py
   │  └─ __init__.py
   ├─ models.py
   ├─ tests.py
   ├─ views.py
   └─ __init__.py

```
```
paperless-system
├─ manage.py
├─ paperless_site
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ __init__.py
├─ README.md
├─ requirements.txt
├─ static
│  └─ assets
│     ├─ .babelrc
│     ├─ css
│     │  ├─ admin_style.css
│     │  ├─ app.css
│     │  ├─ bootstrap.css
│     │  ├─ style.css
│     │  └─ themes
│     │     └─ theme-a.css
│     ├─ favicon.ico
│     ├─ gulpfile.js
│     ├─ images
│     │  └─ capitol.png
│     ├─ img
│     │  ├─ bg1.jpg
│     │  ├─ bg10.jpg
│     │  ├─ bg2.jpg
│     │  ├─ bg3.jpg
│     │  ├─ bg4.jpg
│     │  ├─ bg5.jpg
│     │  ├─ bg6.jpg
│     │  ├─ bg7.jpg
│     │  ├─ bg8.jpg
│     │  ├─ bg9.jpg
│     │  ├─ capitol_logo.png
│     │  ├─ dummy.png
│     │  ├─ lock-bg.jpg
│     │  ├─ logo-single.png
│     │  ├─ logo.png
│     │  ├─ mb-sample.jpg
│     │  ├─ mockup.png
│     │  ├─ profile-bg.jpg
│     │  └─ user
│     │     ├─ 01.jpg
│     │     ├─ 02.jpg
│     │     ├─ 03.jpg
│     │     ├─ 04.jpg
│     │     ├─ 05.jpg
│     │     ├─ 06.jpg
│     │     ├─ 07.jpg
│     │     ├─ 08.jpg
│     │     ├─ 09.jpg
│     │     ├─ 10.jpg
│     │     ├─ 11.jpg
│     │     ├─ 12.jpg
│     │     └─ 13.jpg
│     ├─ js
│     │  ├─ app.init.js
│     │  ├─ app.js
│     │  ├─ custom
│     │  │  └─ custom.js
│     │  ├─ index.js
│     │  └─ modules
│     │     ├─ charts
│     │     │  ├─ chart-knob.js
│     │     │  ├─ chart.js
│     │     │  ├─ chartist.js
│     │     │  ├─ easypiechart.js
│     │     │  ├─ flot.js
│     │     │  ├─ morris.js
│     │     │  ├─ rickshaw.js
│     │     │  └─ sparkline.js
│     │     ├─ common
│     │     │  ├─ bootstrap-start.js
│     │     │  ├─ card-tools.js
│     │     │  ├─ constants.js
│     │     │  ├─ fullscreen.js
│     │     │  ├─ load-css.js
│     │     │  ├─ localize.js
│     │     │  ├─ navbar-search.js
│     │     │  ├─ now.js
│     │     │  ├─ rtl.js
│     │     │  ├─ sidebar.js
│     │     │  ├─ slimscroll.js
│     │     │  ├─ table-checkall.js
│     │     │  ├─ toggle-state.js
│     │     │  ├─ trigger-resize.js
│     │     │  └─ wrapper.js
│     │     ├─ elements
│     │     │  ├─ cards.js
│     │     │  ├─ nestable.js
│     │     │  ├─ notify.js
│     │     │  ├─ porlets.js
│     │     │  ├─ sortable.js
│     │     │  └─ sweetalert.js
│     │     ├─ extras
│     │     │  ├─ calendar.js
│     │     │  ├─ jqcloud.js
│     │     │  └─ search.js
│     │     ├─ forms
│     │     │  ├─ color-picker.js
│     │     │  ├─ forms.js
│     │     │  ├─ imagecrop.js
│     │     │  ├─ select2.js
│     │     │  ├─ upload.js
│     │     │  ├─ wizard.js
│     │     │  └─ xeditable.js
│     │     ├─ maps
│     │     │  ├─ gmap.js
│     │     │  ├─ vector.map.demo.js
│     │     │  └─ vector.map.js
│     │     ├─ pages
│     │     │  └─ pages.js
│     │     └─ tables
│     │        ├─ bootgrid.js
│     │        └─ datatable.js
│     ├─ modernizr-config.json
│     ├─ package-lock.json
│     ├─ package.json
│     ├─ pug
│     │  ├─ views
│     │  │  ├─ charts
│     │  │  │  ├─ chart-chartist.pug
│     │  │  │  ├─ chart-flot.pug
│     │  │  │  ├─ chart-js.pug
│     │  │  │  ├─ chart-morris.pug
│     │  │  │  ├─ chart-radial.pug
│     │  │  │  └─ chart-rickshaw.pug
│     │  │  ├─ dashboard
│     │  │  │  ├─ dashboard.pug
│     │  │  │  ├─ dashboard_h.pug
│     │  │  │  ├─ dashboard_v2.pug
│     │  │  │  └─ dashboard_v3.pug
│     │  │  ├─ elements
│     │  │  │  ├─ buttons.pug
│     │  │  │  ├─ cards.pug
│     │  │  │  ├─ carousel.pug
│     │  │  │  ├─ colors.pug
│     │  │  │  ├─ dropdown-animations.pug
│     │  │  │  ├─ grid-masonry.pug
│     │  │  │  ├─ grid.pug
│     │  │  │  ├─ icons-font.pug
│     │  │  │  ├─ icons-weather.pug
│     │  │  │  ├─ nestable.pug
│     │  │  │  ├─ notifications.pug
│     │  │  │  ├─ portlets.pug
│     │  │  │  ├─ sortable.pug
│     │  │  │  ├─ spinners.pug
│     │  │  │  ├─ sweetalert.pug
│     │  │  │  ├─ template.pug
│     │  │  │  └─ typo.pug
│     │  │  ├─ extras
│     │  │  │  ├─ blog-article-view.pug
│     │  │  │  ├─ blog-articles.pug
│     │  │  │  ├─ blog-post.pug
│     │  │  │  ├─ blog.pug
│     │  │  │  ├─ bug-tracker.pug
│     │  │  │  ├─ calendar.pug
│     │  │  │  ├─ contact-details.pug
│     │  │  │  ├─ contacts.pug
│     │  │  │  ├─ ecommerce-checkout.pug
│     │  │  │  ├─ ecommerce-order-view.pug
│     │  │  │  ├─ ecommerce-orders.pug
│     │  │  │  ├─ ecommerce-product-view.pug
│     │  │  │  ├─ ecommerce-products.pug
│     │  │  │  ├─ faq.pug
│     │  │  │  ├─ file-manager.pug
│     │  │  │  ├─ followers.pug
│     │  │  │  ├─ forum-categories.pug
│     │  │  │  ├─ forum-discussion.pug
│     │  │  │  ├─ forum-topics.pug
│     │  │  │  ├─ help-center.pug
│     │  │  │  ├─ invoice.pug
│     │  │  │  ├─ mailbox.pug
│     │  │  │  ├─ plans.pug
│     │  │  │  ├─ profile.pug
│     │  │  │  ├─ project-details.pug
│     │  │  │  ├─ projects.pug
│     │  │  │  ├─ search.pug
│     │  │  │  ├─ settings.pug
│     │  │  │  ├─ social-board.pug
│     │  │  │  ├─ team-viewer.pug
│     │  │  │  ├─ timeline.pug
│     │  │  │  ├─ todo.pug
│     │  │  │  └─ vote-links.pug
│     │  │  ├─ forms
│     │  │  │  ├─ form-extended.pug
│     │  │  │  ├─ form-imagecrop.pug
│     │  │  │  ├─ form-standard.pug
│     │  │  │  ├─ form-upload.pug
│     │  │  │  ├─ form-validation.pug
│     │  │  │  ├─ form-wizard.pug
│     │  │  │  └─ form-xeditable.pug
│     │  │  ├─ maps
│     │  │  │  ├─ maps-google.pug
│     │  │  │  └─ maps-vector.pug
│     │  │  ├─ multilevel
│     │  │  │  ├─ multilevel-1.pug
│     │  │  │  └─ multilevel-3.pug
│     │  │  ├─ pages
│     │  │  │  ├─ 404.pug
│     │  │  │  ├─ 500.pug
│     │  │  │  ├─ lock.pug
│     │  │  │  ├─ login.pug
│     │  │  │  ├─ maintenance.pug
│     │  │  │  ├─ recover.pug
│     │  │  │  └─ register.pug
│     │  │  ├─ tables
│     │  │  │  ├─ table-bootgrid.pug
│     │  │  │  ├─ table-datatable.pug
│     │  │  │  ├─ table-extended.pug
│     │  │  │  └─ table-standard.pug
│     │  │  ├─ widgets
│     │  │  │  └─ widgets.pug
│     │  │  └─ _partials
│     │  │     ├─ _chat.pug
│     │  │     ├─ _footer.pug
│     │  │     ├─ _footer_page.pug
│     │  │     ├─ _head.pug
│     │  │     ├─ _offsidebar.pug
│     │  │     ├─ _scripts.pug
│     │  │     ├─ _settings.pug
│     │  │     ├─ _sidebar.pug
│     │  │     ├─ _top-navbar.pug
│     │  │     └─ _top-navbar_h.pug
│     │  ├─ _layout.pug
│     │  ├─ _layout_h.pug
│     │  └─ _layout_page.pug
│     ├─ sass
│     │  ├─ app
│     │  │  ├─ charts
│     │  │  │  ├─ chart-easypie.scss
│     │  │  │  ├─ chart-flot.scss
│     │  │  │  └─ radial-bar.scss
│     │  │  ├─ common
│     │  │  │  ├─ animate.scss
│     │  │  │  ├─ bootstrap-custom.scss
│     │  │  │  ├─ bootstrap-reset.scss
│     │  │  │  ├─ button-extra.scss
│     │  │  │  ├─ cards.scss
│     │  │  │  ├─ circles.scss
│     │  │  │  ├─ dropdown-extra.scss
│     │  │  │  ├─ half-float.scss
│     │  │  │  ├─ inputs.scss
│     │  │  │  ├─ placeholder.scss
│     │  │  │  ├─ print.scss
│     │  │  │  ├─ slim-scroll.scss
│     │  │  │  ├─ typo.scss
│     │  │  │  ├─ utils.scss
│     │  │  │  └─ variables.scss
│     │  │  ├─ elements
│     │  │  │  ├─ nestable.scss
│     │  │  │  ├─ notify.scss
│     │  │  │  ├─ portlets.scss
│     │  │  │  └─ spinner.scss
│     │  │  ├─ extras
│     │  │  │  ├─ calendar.scss
│     │  │  │  ├─ mailbox.scss
│     │  │  │  ├─ plans.scss
│     │  │  │  ├─ timeline.scss
│     │  │  │  └─ todo.scss
│     │  │  ├─ forms
│     │  │  │  ├─ dropzone.scss
│     │  │  │  ├─ form-datepicker.scss
│     │  │  │  ├─ form-imgcrop.scss
│     │  │  │  ├─ form-tags.scss
│     │  │  │  ├─ form-validation.scss
│     │  │  │  ├─ form-wizard.scss
│     │  │  │  └─ plugins.scss
│     │  │  ├─ layout
│     │  │  │  ├─ layout-animation.scss
│     │  │  │  ├─ layout-extra.scss
│     │  │  │  ├─ layout.scss
│     │  │  │  ├─ offsidebar.scss
│     │  │  │  ├─ settings.scss
│     │  │  │  ├─ sidebar.scss
│     │  │  │  ├─ top-navbar.scss
│     │  │  │  └─ user-block.scss
│     │  │  ├─ maps
│     │  │  │  ├─ gmap.scss
│     │  │  │  └─ vector-map.scss
│     │  │  └─ tables
│     │  │     ├─ bootgrid.scss
│     │  │     ├─ datatable.scss
│     │  │     └─ table-extras.scss
│     │  ├─ app.scss
│     │  ├─ bootstrap
│     │  │  ├─ bootstrap-grid.scss
│     │  │  ├─ bootstrap-reboot.scss
│     │  │  ├─ bootstrap.scss
│     │  │  ├─ mixins
│     │  │  │  ├─ _alert.scss
│     │  │  │  ├─ _background-variant.scss
│     │  │  │  ├─ _badge.scss
│     │  │  │  ├─ _border-radius.scss
│     │  │  │  ├─ _box-shadow.scss
│     │  │  │  ├─ _breakpoints.scss
│     │  │  │  ├─ _buttons.scss
│     │  │  │  ├─ _caret.scss
│     │  │  │  ├─ _clearfix.scss
│     │  │  │  ├─ _deprecate.scss
│     │  │  │  ├─ _float.scss
│     │  │  │  ├─ _forms.scss
│     │  │  │  ├─ _gradients.scss
│     │  │  │  ├─ _grid-framework.scss
│     │  │  │  ├─ _grid.scss
│     │  │  │  ├─ _hover.scss
│     │  │  │  ├─ _image.scss
│     │  │  │  ├─ _list-group.scss
│     │  │  │  ├─ _lists.scss
│     │  │  │  ├─ _nav-divider.scss
│     │  │  │  ├─ _pagination.scss
│     │  │  │  ├─ _reset-text.scss
│     │  │  │  ├─ _resize.scss
│     │  │  │  ├─ _screen-reader.scss
│     │  │  │  ├─ _size.scss
│     │  │  │  ├─ _table-row.scss
│     │  │  │  ├─ _text-emphasis.scss
│     │  │  │  ├─ _text-hide.scss
│     │  │  │  ├─ _text-truncate.scss
│     │  │  │  ├─ _transition.scss
│     │  │  │  └─ _visibility.scss
│     │  │  ├─ utilities
│     │  │  │  ├─ _align.scss
│     │  │  │  ├─ _background.scss
│     │  │  │  ├─ _borders.scss
│     │  │  │  ├─ _clearfix.scss
│     │  │  │  ├─ _display.scss
│     │  │  │  ├─ _embed.scss
│     │  │  │  ├─ _flex.scss
│     │  │  │  ├─ _float.scss
│     │  │  │  ├─ _interactions.scss
│     │  │  │  ├─ _overflow.scss
│     │  │  │  ├─ _position.scss
│     │  │  │  ├─ _screenreaders.scss
│     │  │  │  ├─ _shadows.scss
│     │  │  │  ├─ _sizing.scss
│     │  │  │  ├─ _spacing.scss
│     │  │  │  ├─ _stretched-link.scss
│     │  │  │  ├─ _text.scss
│     │  │  │  └─ _visibility.scss
│     │  │  ├─ vendor
│     │  │  │  └─ _rfs.scss
│     │  │  ├─ _alert.scss
│     │  │  ├─ _badge.scss
│     │  │  ├─ _breadcrumb.scss
│     │  │  ├─ _button-group.scss
│     │  │  ├─ _buttons.scss
│     │  │  ├─ _card.scss
│     │  │  ├─ _carousel.scss
│     │  │  ├─ _close.scss
│     │  │  ├─ _code.scss
│     │  │  ├─ _custom-forms.scss
│     │  │  ├─ _dropdown.scss
│     │  │  ├─ _forms.scss
│     │  │  ├─ _functions.scss
│     │  │  ├─ _grid.scss
│     │  │  ├─ _images.scss
│     │  │  ├─ _input-group.scss
│     │  │  ├─ _jumbotron.scss
│     │  │  ├─ _list-group.scss
│     │  │  ├─ _media.scss
│     │  │  ├─ _mixins.scss
│     │  │  ├─ _modal.scss
│     │  │  ├─ _nav.scss
│     │  │  ├─ _navbar.scss
│     │  │  ├─ _pagination.scss
│     │  │  ├─ _popover.scss
│     │  │  ├─ _print.scss
│     │  │  ├─ _progress.scss
│     │  │  ├─ _reboot.scss
│     │  │  ├─ _root.scss
│     │  │  ├─ _spinners.scss
│     │  │  ├─ _tables.scss
│     │  │  ├─ _toasts.scss
│     │  │  ├─ _tooltip.scss
│     │  │  ├─ _transitions.scss
│     │  │  ├─ _type.scss
│     │  │  ├─ _utilities.scss
│     │  │  └─ _variables.scss
│     │  ├─ bootstrap.scss
│     │  └─ themes
│     │     ├─ theme-a.scss
│     │     ├─ theme-b.scss
│     │     ├─ theme-c.scss
│     │     ├─ theme-d.scss
│     │     ├─ theme-e.scss
│     │     ├─ theme-f.scss
│     │     ├─ theme-g.scss
│     │     └─ theme-h.scss
│     ├─ server
│     │  ├─ datatable.json
│     │  ├─ i18n
│     │  │  ├─ site-en.json
│     │  │  └─ site-es.json
│     │  └─ xeditable-groups.json
│     ├─ sidebar.json
│     ├─ vendor
│     │  ├─ bootstrap
│     │  │  └─ dist
│     │  │     └─ bootstrap.js
│     │  ├─ jquery
│     │  │  └─ dist
│     │  │     └─ jquery.js
│     │  ├─ jquery-slimscroll
│     │  │  └─ jquery.slimscroll.js
│     │  └─ js-storage
│     │     └─ js.storage.js
│     └─ vendor.json
├─ templates
│  ├─ admin_dashboard.html
│  ├─ admin_login.html
│  ├─ base.html
│  ├─ dashboard.html
│  ├─ head_dashboard.html
│  ├─ head_login.html
│  ├─ includes
│  │  ├─ admin_sidebar.html
│  │  ├─ employee_sidebar.html
│  │  ├─ governor_sidebar.html
│  │  └─ head_sidebar.html
│  ├─ login.html
│  └─ register.html
└─ tracking
   ├─ admin.py
   ├─ apps.py
   ├─ migration
   │  └─ __init__.py
   ├─ migrations
   │  ├─ 0001_initial.py
   │  ├─ 0002_alter_department_id_alter_userprofile_id.py
   │  └─ __init__.py
   ├─ models.py
   ├─ tests.py
   ├─ views.py
   └─ __init__.py

```
;(function ( $, window, document, undefined ) {

    "use strict";

    // window and document are passed through as local variable rather than global
    // as this (slightly) quickens the resolution process and can be more efficiently
    // minified (especially when both are regularly referenced in your plugin).

    // Create the defaults once
    var pluginName = "dynalist",
        defaults = {
            itemStoreId: "id_answers",
            correctStoreId: "id_correct_answer"
        };

    // The actual plugin constructor
    function Plugin ( element, options ) {
        this.element = element;
        this.$el = $(element);
        this.settings = $.extend( {}, defaults, options );
        this._defaults = defaults;
        this._name = pluginName;
        this.ENTER_KEY = 13;
        this.ESCAPE_KEY = 27;

        this.init();
    }

    // Avoid Plugin.prototype conflicts
    $.extend(Plugin.prototype, {
        init: function () {
            this.items = [];
            this.correctIndex = -1;
            this.correctId = '';
            this.cacheElements();
            this.bindEvents();
            this.setupItems();
            this.render();
        },
        uuid: function () {
            /*jshint bitwise:false */
            var i, random;
            var uuid = '';

            for (i = 0; i < 32; i++) {
                random = Math.random() * 16 | 0;
                if (i === 8 || i === 12 || i === 16 || i === 20) {
                    uuid += '-';
                }
                uuid += (i === 12 ? 4 : (i === 16 ? (random & 3 | 8) : random)).toString(16);
            }

            return uuid;
        },
        storeItems: function () {
            var items = [];
            for (var i=0; i<this.items.length; i++) {
                items.push(this.items[i].title);
            }
            this.$itemStore.val(items.join(","));
            if (this.correctIndex >= 0)
                this.$correctStore.val(this.correctIndex + 1);
        },
        cacheElements: function () {
            this.itemTemplate = this.$el.find('.item-template').html();
            this.$newItem = this.$el.find('.new-item');
            this.$itemList = this.$el.find('.item-list');
            this.$itemStore = $('#' + this.settings.itemStoreId);
            this.$correctStore = $('#' + this.settings.correctStoreId);
        },
        bindEvents: function () {
            var list = this.$itemList;
            this.$newItem.on('keypress', this.create.bind(this));
            list.on('change', '.toggle', this.toggle.bind(this));
            list.on('dblclick', 'label', this.edit.bind(this));
            list.on('keypress', '.edit', this.editKeyup.bind(this));
            list.on('focusout', '.edit', this.update.bind(this));
            list.on('click', '.destroy', this.destroy.bind(this));
        },
        setupItems: function(){
            var $this = this;

            this.$itemList.find("li").each(function(e) {
                var uuid = $this.uuid();
                var item = {
                    id: $(this).attr('id') || uuid,
                    title: $(this).find('label').html()
                };
                if (!$(this).attr('id')) $(this).attr('id', uuid);
                $this.items.push(item);
            });
            this.correctIndex = parseInt(this.$correctStore.val(), 10);
            if (this.correctIndex) {
                this.correctIndex -= 1;
                if (this.correctIndex < 0) this.correctIndex = 0;
                if (this.correctIndex > this.items.length) this.correctIndex = this.items.length;
                if (this.items.length)
                    this.correctId = this.items[this.correctIndex].id;
                else
                    this.correctId = "";
            } else
                this.correctId = "";
            this.storeItems();
        },
        render: function () {
            var html = [];
            for (var i=0; i<this.items.length; i++) {
                html.push(this.nanoTmpl(this.itemTemplate, this.items[i]));
            }
            this.$itemList.html(html.join(''));

            if(this.items.length) {
                if (this.correctIndex >= 0 && this.correctId !== "") {
                    if(this.items[this.correctIndex].id !== this.correctId) {
                        // Index and Id mismatch. Switch to the first item
                        this.correctIndex = 0;
                        this.correctId = this.items[this.correctIndex].id;
                        this.storeItems();
                    }
                } else if (this.correctIndex >= 0 && this.correctId === "") {
                    this.correctId = this.items[this.correctIndex].id;
                    this.storeItems();
                } else {
                    this.correctIndex = 0;
                    this.correctId = this.items[this.correctIndex].id;
                    this.storeItems();
                }
            }

            $('#' + this.correctId).find(".toggle").prop('checked', true);
        },
        indexFromId: function(id){
            var items = this.items;
            var i = items.length;

            while (i--) {
                if (items[i].id === id) {
                    return i;
                }
            }
        },
        // accepts an element from inside the `.item` div and
        // returns the corresponding index in the `todos` array
        indexFromEl: function (el) {
            var id = $(el).closest('li').attr('id');
            var items = this.items;
            var i = items.length;

            while (i--) {
                if (items[i].id === id) {
                    return i;
                }
            }
        },
        create: function (e) {
            var $input = $(e.target);
            var val = $input.val().trim();

            if (e.which !== this.ENTER_KEY || !val) {
                return;
            }
            e.preventDefault();
            var newItem = {
                id: this.uuid(),
                title: val
            };
            this.items.push(newItem);
            this.storeItems();

            $input.val('');

            this.render();
        },
        toggle: function (e) {
            var idx = this.indexFromEl(e.target);
            if ($(e.target).prop('checked')) {
                // Change the selected id and alter the others
                this.correctIndex = idx;
                this.correctId = this.items[idx].id;
            }
            this.storeItems();
            this.render();
        },
        edit: function (e) {
            var $li = $(e.target).closest('li'),
                $input = $li.addClass('editing').find('.edit'),
                $destroy = $li.find('.destroy').prop('disabled', true);
            $input.val($input.val()).focus();
        },
        editKeyup: function (e) {
            if (e.which === this.ENTER_KEY) {
                e.preventDefault();
                e.target.blur();
            }

            if (e.which === this.ESCAPE_KEY) {
                $(e.target).data('abort', true).blur();
                e.preventDefault();
            }
        },
        update: function (e) {
            var el = e.target,
                $el = $(el),
                val = $el.val().trim(),
                idx = this.indexFromEl(e.target),
                $destroy = $el.closest('.destroy').prop('disabled', false);

            if ($el.data('abort')) {
                $el.data('abort', false);
                this.render();
                return;
            }
            var i = idx;

            if (val) {
                this.items[i].title = val;
            } else {
                this.items.splice(i, 1);
            }
            this.storeItems();
            this.render();
        },
        destroy: function (e) {
            var idx = this.indexFromEl(e.target);
            this.items.splice(idx, 1);
            if (this.items[this.correctIdx] !== this.items[idx]) {
                this.correctIndex = 0;
                this.correctId = this.items[0].id;
            }
            this.storeItems();
            this.render();
        },
        /* Nano Templates - https://github.com/trix/nano */

        nanoTmpl: function (template, data) {
            return template.replace(/\{\{([\w\.]*)\}\}/g, function(str, key) {
                var keys = key.split("."), v = data[keys.shift()];
                for (var i = 0, l = keys.length; i < l; i++) v = v[keys[i]];
                return (typeof v !== "undefined" && v !== null) ? v : "";
            });
        }

    });

    // A really lightweight plugin wrapper around the constructor,
    // preventing against multiple instantiations
    $.fn[ pluginName ] = function ( options ) {
        return this.each(function() {
            if ( !$.data( this, "plugin_" + pluginName ) ) {
                $.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
            }
        });
    };

})( django.jQuery, window, document );

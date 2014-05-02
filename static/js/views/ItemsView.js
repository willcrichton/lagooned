define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/items.html'));

    return Backbone.View.extend({
        el: '#items',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },

        render: function() {
            var items = $.extend({}, GAME.me.get('items'));

            var has_items = false;
            for (var k in items) {
                has_items = true;
                if (items[k].qty > 0) {
                    items[k.toLowerCase().replace(' ', '')] = items[k];
                }

                delete items[k];
            }

            if (!has_items) {
                this.$el.hide();
                return this;
            } else {
                this.$el.show();
            }

            this.$el.html(template({
                items: items
            }));

            $(".qtip").remove();
            this.$('.item').qtip({
                style: { classes: 'qtip-light' },
                position: {
                    my: 'top center',
                    at: 'bottom center'
                }
            });

            return this;
        }
    });
});

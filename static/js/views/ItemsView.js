define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/items.html'));

    return Backbone.View.extend({
        el: '#items',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },

        render: function() {
            var items = GAME.me.get('items'); 
            for (var k in items) {
                if (items[k].qty > 0) {
                    items[k.toLowerCase().replace(' ', '')] = items[k];
                }

                delete items[k];
            }

            this.$el.html(template({
                items: items
            }));

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

define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/items.html'));

    return Backbone.View.extend({
        el: '#items',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },

        render: function() {
            this.$el.html(template({
                items: GAME.me.get('items')
            }));

            return this;
        }
    });
});

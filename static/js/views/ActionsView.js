define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/actions.html'));

    return Backbone.View.extend({
        el: '#actions',

        events: {
            'click .action': 'doAction'
        },

        initialize: function() {
            this.listenTo(GAME.actions, 'add remove change reset', this.render);
            this.listenTo(GAME.me, 'change', this.render)
        },

        doAction: function(e) {
            var action = $(e.target).data('action');
            GAME.doAction(action);
        },

        render: function() {
            this.$el.html(template({
                actions: GAME.actions.toJSON(),
                user: GAME.me.toJSON()
            }));

            return this;
        }
    });
});

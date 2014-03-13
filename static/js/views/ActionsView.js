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
            var duration = 0;
            GAME.actions.forEach(function(a) {
                if (a.get('name') == action) {
                    duration = a.get('duration');
                }
            });

            GAME.doAction(action);

            var time = new Date().getTime();
            var timer = setInterval(function() {
                var diff = (new Date().getTime() - time) / 1000;
                var percent = diff / duration * 100;
                $(e.target).css('background', 'linear-gradient(to right, rgba(0, 0, 0, 0.1) ' + percent + '%, transparent ' + percent + '%)')
            }, 10);

            setTimeout(function() {
                clearInterval(timer);
                $(e.target).css('background', 'transparent');
            }, duration * 1000);
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

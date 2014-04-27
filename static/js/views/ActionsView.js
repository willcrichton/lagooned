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
            this.listenTo(GAME.me, 'change', this.render);
            this.listenTo(GAME.me, 'action', this.onAction);
            this.lock = false;
        },

        doAction: function(e) {
            //if (this.lock) return;

            var action = $(e.target).data('action');
            var duration = 0;
            GAME.actions.forEach(function(a) {
                if (a.get('name') == action) {
                    duration = a.get('duration');
                }
            });
 
            this.curTarget = $(e.target);
            this.curDuration = duration;
            GAME.doAction(action);
        },

        onAction: function() {
            this.lock = true;

            var time = new Date().getTime();
            var timer = setInterval(_.bind(function() {
                var diff = (new Date().getTime() - time) / 1000;
                var percent = diff / this.curDuration * 100;
                this.curTarget.css('background', 'linear-gradient(to right, rgba(0, 0, 0, 0.1) ' + percent + '%, rgba(255, 255, 255, 0.3) ' + percent + '%)')
            }, this), 10);

            setTimeout(_.bind(function() {
                clearInterval(timer);
                this.curTarget.css('background', 'transparent');
                this.lock = false;
            }, this), this.curDuration * 1000);
        },

        render: function() {
            var actions = GAME.actions.toJSON();
            var new_actions = {};
            
            actions.forEach(function(action) {
                if (!new_actions[action.category]) 
                    new_actions[action.category] = [];
                
                new_actions[action.category].push(action);
            });

            this.$el.html(template({
                actions: new_actions
            }));

            return this;
        }
    });
});

define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/log.html'));

    return Backbone.View.extend({
        el: '#log',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },
        
        render: function() {
            this.$el.html(template({
                'log': GAME.me.get('log').reverse()
            }));

            return this;
        }
    });
});

define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/stats.html'));

    return Backbone.View.extend({
        el: '#stats',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },

        render: function() {
            this.$el.html(template(GAME.me.toJSON()));
            return this;
        }
    });
});

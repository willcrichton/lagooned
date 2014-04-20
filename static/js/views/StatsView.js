define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/stats.html'));

    return Backbone.View.extend({
        el: '#stats',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },

        render: function() {
            var food = GAME.me.get('food');
            if (food == 0) food = "Starving";
            else if (food < 5) food = "Hungry";
            else if (food < 10) food = "Normal";
            else food = "Satisfied";
            this.$el.html(template({food: food}));
            return this;
        }
    });
});

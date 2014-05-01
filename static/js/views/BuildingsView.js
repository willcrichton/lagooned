define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/buildings.html'));
    
    return Backbone.View.extend({
        el: '#buildings',

        initialize: function() {
            this.listenTo(GAME.me, 'change', this.render);
        },

        render: function() {
            var has_fire = false, has_leanto = false;
            var buildings = GAME.me.get('buildings');
            for (var i = 0; i < buildings.length; i++) {
                if (buildings[i] == 'BUILDING_LEANTO') has_leanto = true;
                if (buildings[i] == 'BUILDING_FIRE') has_fire = true;
            }

            this.$el.html(template({
                has_fire: has_fire,
                has_leanto: has_leanto
            }));

            return this;
        }
    });
});
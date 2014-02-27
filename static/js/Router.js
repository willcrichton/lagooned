define(function(require) {
    'use strict';

    var HomeView  = require('views/HomeView'),
        StartView = require('views/StartView'),
        IntroView = require('views/IntroView'),
        User      = require('models/User');

    return Backbone.Router.extend({
        routes: {
            'start' : 'start',
            'home'  : 'home',            
            'intro' : 'intro',
        },

        initialize: function() {
            this.currentView = null;
        },

        swapViews: function(View) {
            var view = new View();
            view.router = this;

            var swap = _.bind(function() {
                $('body').html(view.render().el);
                this.currentView = view;
                this.trigger('changeView');

                $('body').fadeIn(1000);
            }, this);

            if (this.currentView) {
                $('body').fadeOut(1000, _.bind(function() {
                    this.currentView.remove();
                    swap();
                }, this));
            } else {
                swap();
            }
        },

        start: function() {
            this.swapViews(StartView);
        },

        home: function() {
            this.swapViews(HomeView);
        },

        intro: function() {
            this.swapViews(IntroView);
        }
    });
});

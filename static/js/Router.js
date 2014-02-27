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
            'new'   : 'newGame'
        },

        initialize: function() {
            this.currentView = null;
        },

        swapViews: function(View) {
            if (this.currentView) {
                this.currentView.remove();
            }

            var view = new View();
            $('body').html(view.render().el);
            this.currentView = view;
            this.trigger('changeView');
        },

        start: function() {
            this.swapViews(StartView);
        },

        home: function() {
            this.swapViews(HomeView);
        },

        intro: function() {
            this.swapViews(IntroView);
        },
        
        newGame: function() {
            var newU = new User({name: 'HelloWorld'});            
            newU.save();
            this.navigate('intro', {trigger: true});
        }
    });
});

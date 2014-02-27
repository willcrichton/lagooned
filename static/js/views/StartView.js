define(function(require) {
    'use strict';

    var User = require('models/User');
    var template = Handlebars.compile(require('text!templates/start.html'));

    return Backbone.View.extend({
        events: { 
            'click #start' : 'start',
            'click #login' : 'login',
            'keyup input'  : 'submit'
        },
        
        start: function(e) {
            e.preventDefault();

            // show new user form when they click "start"
            this.$('#links').fadeOut(function() {
                $('#input').fadeIn();
            });
        },

        login: function(e) {
            e.preventDefault();
            this.$('#links').fadeOut(function() {
                // TODO: have a login form
            });
        },

        submit: function(e) {
            // 13 = key code for enter
            if (e.which != 13) return;
                
            var newU = new User({name: this.$('input[type=text]').val()});
            newU.save();
            this.router.navigate('intro', {trigger: true});
        },

        render: function() {
            this.$el.html(template);
            return this;
        }
    });
});

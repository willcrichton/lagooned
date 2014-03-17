define(function(require) {
    'use strict';

    var User = require('models/User');
    var template = Handlebars.compile(require('text!templates/start.html'));

    return Backbone.View.extend({
        events: { 
            'click #start'  : 'start',
            'click #login'  : 'login',
            'keyup input'   : 'submit',
            'click #submit' : 'submit'
        },

        initialize: function() {
            this.newUser = false;
        },
        
        start: function(e) {
            e.preventDefault();

            // show new user form when they click "start"
            this.newUser = true;
            this.$('#links').fadeOut(function() {
                $('#input').fadeIn();
            });
        },

        login: function(e) {
            e.preventDefault();
            this.$('#links').fadeOut(function() {
                //$('#input').fadeIn();
                alert('Go bug Will to implement this (or do it yourself!)');
            });
        },

        submit: function(e) {
            // 13 = key code for enter
            if (e.type != 'click' && e.which != 13) return;

            if (this.newUser) {
                GAME.me.set({
                    name: this.$('#name').val(),
                    password: this.$('#password').val(),
                    login: !this.newUser
                }).save().done(_.bind(function() {
                    GAME.actions.fetch().done(_.bind(function() {
                        this.router.navigate('intro', {trigger: true});
                    }, this));
                }, this));
            } else {
                GAME.me.set({
                    name: this.$('#name').val(),
                    password: this.$('#password').val(),
                    login: !this.newUser
                }).fetch().done(_.bind(function() {
                    if (!GAME.me.id) {
                        alert('Login fail');
                    } else {
                        this.router.navigate('home', {trigger: true});
                    }
                }, this));
            }
        },

        render: function() {
            this.$el.html(template);
            return this;
        }
    });
});

var GAME = {};

define(function(require){
    'use strict';

    requirejs.config({
        enforceDefine: true,
        inlineText: true,
        urlArgs: "bust=" + (new Date()).getTime()
    });

    var Router  = require('Router'),
        User    = require('models/User'),
        Actions = require('collections/Actions');

    // load cookie from storage
    if (localStorage.TOKEN) {
        TOKEN = localStorage.TOKEN;
    }

    // have our models sync up over websockets instead of using $.ajax
    Backbone.sync = function(method, model, options) {
        if (typeof options == 'function') {
            options = { success: options, error: error };
        }

        var ws = new WebSocket("ws://" + document.domain + ":5000/socket");

        ws.onopen = function() {
            var id = Math.random().toString(36).slice(2);
            var toSend = {model: model.toJSON(), 
                          method: method, 
                          id: id, 
                          className: model.className,
                          token: TOKEN};

            ws.send(JSON.stringify(toSend));
        }

        var $promise = $.Deferred();
        ws.onmessage = function(event) {
            var data = JSON.parse(event.data);
            console.log(data);

            if (data['token']) {
                TOKEN = data['token'];
                localStorage.TOKEN = TOKEN;
            }

            options.success(data);
            $promise.resolve();
        }

        return $promise;
    }

    GAME.socket = new WebSocket("ws://" + document.domain + ":5000/socket");
    GAME.socket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        if ('success' in data) {
            if (data.success) {
                console.log('Action valid');
                GAME.me.trigger('action');
            } else {
                console.log('Action invalid');
            }
        } else {
            GAME.me.set(data.user);
            GAME.actions.set(data.actions);
        }
    }

    GAME.actions = new Actions();
    GAME.actions.fetch();

    GAME.doAction = function(action) {
        GAME.socket.send(JSON.stringify({
            action: action,
            method: 'action',
            token: TOKEN
        }));
    };

    // load in user data
    GAME.me = new User();
    GAME.me.fetch().done(function() {

        // set up router and let it take over
        var appRouter = new Router();
        
        Backbone.history.start();
        
        // if (!me.id) then they're not logged in
        if (!GAME.me.id) {
            appRouter.navigate('start', {trigger: true});
        } else {
            GAME.actions.fetch();
            appRouter.navigate('home', {trigger: true});
        }

        $('#background').attr('class', GAME.me.get('location'));
    });
});

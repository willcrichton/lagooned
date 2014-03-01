define(function(require){
    'use strict';

    requirejs.config({
        enforceDefine: true,
        inlineText: true,
        urlArgs: "bust=" + (new Date()).getTime()
    });

    var Router = require('Router'),
        User   = require('models/User');

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
            options.success(JSON.parse(event.data));
            $promise.resolve();
        }

        return $promise;
    }

    var mainSocket = new WebSocket("ws://" + document.domain + ":5000/socket");
    mainSocket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        console.log(data);
    }
    
    // load in user data
    var me = new User();
    me.fetch().done(function() {
            
        // set up router and let it take over
        var appRouter = new Router();
        
        Backbone.history.start();
        
        // if (!me.id) then they're not logged in
        if (!me.id) {
            appRouter.navigate('start', {trigger: true});
        } else {
            appRouter.navigate('home', {trigger: true});
        }
    });
});

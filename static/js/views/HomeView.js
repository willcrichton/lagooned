define(function(require) {
    'use strict';

    var ActionsView   = require('views/ActionsView'),
        LogView       = require('views/LogView'),
        ItemsView     = require('views/ItemsView'),
        BuildingsView = require('views/BuildingsView');

    var template = Handlebars.compile(require('text!templates/home.html'));
    var GAIN = 0.3;

    return Backbone.View.extend({
        initialize: function() {
            var context = new webkitAudioContext();
            var nodes = {};
            var sounds = ['/static/sounds/ocean.mp3', '/static/sounds/forest.mp3'];
            var locations = ['beach', 'forest', 'cave'];

            // load all ambience and create audio nodes
            var loader = new BufferLoader(context, sounds, function(list) {
                for (var i = 0; i < list.length; i++) {
                    var source = context.createBufferSource();
                    source.buffer = list[i];
                    source.loop = true;
                    source.start(0);
                    
                    var gain = context.createGainNode();
                    gain.gain.value = GAME.me.get('location') == locations[i] ? GAIN : 0.0;
                    source.connect(gain);
                    gain.connect(context.destination);

                    nodes[locations[i]] = gain;
                }
            });

            loader.load();

            this.listenTo(GAME.me, 'change', function() {
                var location = GAME.me.get('location');
                var old_location = $('#background').attr('class');
                if (location == '' || location == old_location) return;
                if (old_location != '') { 

                    // crossfade between tracks
                    var start = new Date().getTime();
                    var timer = setInterval(function() {
                        var x = (new Date().getTime() - start) / 2000;
                        nodes[old_location].gain.value = Math.cos(x * 0.5 * Math.PI) * GAIN;
                        nodes[location].gain.value = Math.cos((1.0 - x) * 0.5 * Math.PI) * GAIN;

                        if (x >= 1.0) {
                            clearInterval(timer);
                        }
                    }, 10);
                } else {
                    nodes[location].gain.value = GAIN;
                }

                $('#background').attr('class', location);
            });
        },
        
        render: function() {
            this.$el.html(template);

            // load subviews
            this.actionsView = new ActionsView().render();
            this.logView = new LogView().render();
            this.itemsView = new ItemsView().render();
            this.buildingsView = new BuildingsView().render();

            // set height of bg to viewport size
            this.$('#background').css('height', window.innerHeight);
            $(window).resize(function() {
                this.$('#background').css('height', window.innerHeight);
            });

            return this;
        }
    });
});

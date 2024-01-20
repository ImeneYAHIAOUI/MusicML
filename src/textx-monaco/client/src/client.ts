/* --------------------------------------------------------------------------------------------
 * Copyright (c) 2018 TypeFox GmbH (http://www.typefox.io). All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
import { listen } from '@codingame/monaco-jsonrpc';
import * as monaco from 'monaco-editor-core'
import {
    MonacoLanguageClient, MessageConnection, CloseAction, ErrorAction,
    MonacoServices, createConnection
} from '@codingame/monaco-languageclient';
import normalizeUrl = require('normalize-url');
const ReconnectingWebSocket = require('reconnecting-websocket');

// register Monaco languages
monaco.languages.register({
    id: 'json',
    extensions: ['.json', '.bowerrc', '.jshintrc', '.jscsrc', '.eslintrc', '.babelrc'],
    aliases: ['JSON', 'json'],
    mimetypes: ['application/json'],
});

// create Monaco editor
const value = `MusicPiece BillieJean
Author 'Michael Jackson'

DefaultTempo 116 bpm

DefaultTimeSignature 4/4

Track Drum Instrument 3 // And this is a semantic error
`;
const containerElement = document.getElementById("container")!;

const newButton = document.createElement("button");
newButton.textContent = "clear";
document.body.appendChild(newButton);

const monacoEditor = monaco.editor.create(containerElement, {
    model: monaco.editor.createModel(value, 'json', monaco.Uri.parse('inmemory://model.json')),
    glyphMargin: true,
    lightbulb: {
        enabled: true
    }
});



newButton.addEventListener('click', function () {
    monacoEditor.setValue('');
});


MonacoServices.install(monaco);

// create the web socket
const url = createUrl(`${location.hostname}:3001`);
const webSocket = createWebSocket(url);
// listen when the web socket is opened
listen({
    webSocket,
    onConnection: connection => {
        // create and start the language client
        const languageClient = createLanguageClient(connection);
        const disposable = languageClient.start();
        connection.onClose(() => disposable.dispose());
    }
});

function createLanguageClient(connection: MessageConnection): MonacoLanguageClient {
    return new MonacoLanguageClient({
        name: "Sample Language Client",
        clientOptions: {
            // use a language id as a document selector
            documentSelector: ['json'],
            // disable the default error handler
            errorHandler: {
                error: () => ErrorAction.Continue,
                closed: () => CloseAction.DoNotRestart
            }
        },
        // create a language client connection from the JSON RPC connection on demand
        connectionProvider: {
            get: (errorHandler, closeHandler) => {
                return Promise.resolve(createConnection(connection, errorHandler, closeHandler))
            }
        }
    });
}

function createUrl(path: string): string {
    const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
    return normalizeUrl(`${protocol}://${path}`);
}

function createWebSocket(url: string): WebSocket {
    const socketOptions = {
        maxReconnectionDelay: 10000,
        minReconnectionDelay: 1000,
        reconnectionDelayGrowFactor: 1.3,
        connectionTimeout: 10000,
        maxRetries: Infinity,
        debug: false
    };
    return new ReconnectingWebSocket(url, [], socketOptions);
}

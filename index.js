const qrcode = require('qrcode-terminal');
const axios = require('axios');
const FormData = require('form-data');

const { Client, MessageMedia, Location, MessageButton, Button, ButtonsMessage, Buttons } = require('whatsapp-web.js');
const client = new Client();
//const { Message, ClientInfo, Buttons } = require('whatsapp-web.js/src/structures');

let userStates = {};

const questions = {
    1: 'Bem vindo ao formulário de Denúncia de enchentes. Por favor, responda as perguntas abaixo: \n\nPrimeiro, envie uma foto ou vídeo do local da enchente.',
    2: {
        text : 'Qual parte de Heliópolis aconteceu a enchente?',
        options: {
            1: 'Mina',
            2: 'Lagoa',
            3: 'Portuguesa',
            4: 'Heliópolis',
            5: 'Imperador/Pilões',
            6: 'Redondinhos',
            7: 'Paquistão',
            8: 'Cohab',
        }
    },
    3: {
        text: 'Quando aconteceu a enchente?',
        options: {
            1: 'Hoje',
            2: 'Ontem',
            3: 'Anteontem',
            4: 'Outro',
        }
    },
    4 : 'Qual seu nome?',
    5 : 'Se quiser, conte um pouco sobre como foi seu dia durante a enchente. Caso não queira, digite "não".',
};



client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', msg => {
    if (msg.body == '!ping') {
        msg.reply('pong');
    }
});

client.on('message', msg => {
    if (msg.body == '!website') {
        msg.reply('https://www.google.com');
    }
});

client.on('message', msg => {
    if (msg.body === '!formulario') {
        userStates[msg.from] = {
            currentQuestion: 1,
            answers: {}
        };
        msg.reply(formatQuestion(questions[1]));
    } else if (userStates[msg.from]) {
        const state = userStates[msg.from];
        const currentQuestion = questions[state.currentQuestion];

        if (typeof currentQuestion !== 'string' && currentQuestion.options) {
            if (!currentQuestion.options[msg.body]) {
                msg.reply('Ops, não entendi sua resposta. Por favor, tente novamente com uma das opções numericas listadas acima.');
                return;
            }
        }

        state.answers[state.currentQuestion] = msg.body;
        state.currentQuestion++;

        if (questions[state.currentQuestion]) {
            msg.reply(formatQuestion(questions[state.currentQuestion]));
        } else {
            msg.reply('Obrigado pelas respostas! Sua denúncia foi enviada para a equipe de voluntários.');
            console.log(state.answers);
            delete userStates[msg.from];
        }
    }
});

function formatQuestion(question) {
    if (typeof question === 'string') {
        return question;
    } else {
        let options = '';
        for (const [key, value] of Object.entries(question.options)) {
            options += `${key} - ${value}\n`;
        }
        return `${question.text}\n${options}`;
    }
}
// test command with buttons
client.on('message', async msg => {
    if (msg.body === '!buttons') {
        const buttons = [
            { buttonId: 'id1', buttonText: { displayText: 'Button 1' }, type: 1 },
            { buttonId: 'id2', buttonText: { displayText: 'Button 2' }, type: 1 }
        ];

        const buttonMessage = {
            contentText: 'Hi! This is a button message.',
            footerText: 'This is a footer text',
            buttons: buttons,
            headerType: 1,
        };

        await client.sendMessage(msg.from, buttonMessage);
    }
});




client.on('message', async msg => {
    if (msg.body === '!pic') {

        const media = await MessageMedia.fromUrl('https://via.placeholder.com/350x150.png');

        chat.sendMessage(media);
    }
});

    

client.on('ready', () => {
    console.log('Client is ready!');
});


client.initialize();
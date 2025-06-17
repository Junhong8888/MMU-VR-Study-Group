
import { addConnectionStateHandler } from './main.js';

let socket;
let localStream;
let peerConnection;
let dataChannel;

async function start(username) {
    // Get local media first
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    document.getElementById('localVideo').srcObject = localStream;

    // Setup WebSocket
    socket = new WebSocket("ws://" + window.location.host + "/ws/chat/testchannel/");
    socket.onopen = () => console.log("WebSocket connection established.");

    // Setup peer connection AFTER getting media
    setupPeerConnection(username);

    // Handle incoming WebSocket messages
    socket.onmessage = async (e) => {
        console.log("WebSocket message received:", e.data); // Add logging here
        const data = JSON.parse(e.data);
    
        if (data.type === "sdp") {
            const sdp = new RTCSessionDescription(data.sdp);
            if (sdp.type === "offer" && username === "callee") {
                console.log("Received offer from caller.");
                await peerConnection.setRemoteDescription(sdp);
                const answer = await peerConnection.createAnswer();
                await peerConnection.setLocalDescription(answer);
                socket.send(JSON.stringify({ type: "sdp", sdp: peerConnection.localDescription }));
            } else if (sdp.type === "answer" && username === "caller") {
                console.log("Received answer from callee.");
                await peerConnection.setRemoteDescription(sdp);
            }
        } else if (data.type === "ice") {
            try {
                await peerConnection.addIceCandidate(data.candidate);
            } catch (err) {
                console.error("Error adding ICE candidate", err);
            }
        } else if (data.type === "chat") {
            console.log("Received chat message:", data.message);
        }
    };

    // Caller starts the offer
    if (username === "caller") {
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        socket.send(JSON.stringify({ type: "sdp", sdp: peerConnection.localDescription }));
    }
}

function setupPeerConnection(username) {
    peerConnection = new RTCPeerConnection({
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
    });

    addConnectionStateHandler(peerConnection, username);

    // Add local tracks
    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    });

    // Receive remote track
    peerConnection.ontrack = (event) => {
        console.log("Remote track received:", event); // Log remote track
        const remoteVideo = document.getElementById("remoteVideo");
        if (remoteVideo) {
            remoteVideo.srcObject = event.streams[0]; // Attach the remote stream
        }
    };

    // Send ICE candidates
    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            console.log("Sending ICE candidate:", event.candidate); // Log ICE candidate
            socket.send(JSON.stringify({ type: "ice", candidate: event.candidate }));
        }
    };

    // Optional: data channel (only caller creates it)
    if (username === "caller") {
        dataChannel = peerConnection.createDataChannel("chat");
    } else {
        peerConnection.ondatachannel = event => {
            dataChannel = event.channel;
        };
    }
}

export { start };



/*
async function start(username) {
    // Initialize the WebSocket connection to send signaling data.
    socket = new WebSocket("ws://" + window.location.host + "/ws/chat/testchannel/");

    socket.onopen = function () {
        console.log("WebSocket connection established.");
    };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.type === "sdp") {
            handleSDP(data.sdp, username);
        } else if (data.type === "chat") {
            console.log("Received chat message:", data.message);
        }
    };

    const [peerConnection, dataChannel] = initializeBeforeCreatingOffer(username);
    withPerfectNegociationHandler(async sessionDescriptionProtocol => {
        if (sessionDescriptionProtocol.type === "offer") {
            await beCallee(sessionDescriptionProtocol, peerConnection, username, dataChannel);
        } else {
            await beCaller(sessionDescriptionProtocol, peerConnection, dataChannel);
        }
    }, peerConnection, username, dataChannel);

    firstNegotiationNeededEvent(peerConnection, dataChannel);

    if (username === "impolite") {
        await sleep(5000);
        secondNegotiationNeededEvent(peerConnection);
    }
}

function initializeBeforeCreatingOffer(username) {
    const peerConnection = { obj: initializeRTCPeerConnection(username) };
    const dataChannel = { obj: null };

    return [peerConnection, dataChannel];
}

function initializeRTCPeerConnection(username) {
    const peerConnection = new RTCPeerConnection();
    common.addConnectionStateHandler(peerConnection, username);
    peerConnection.ontrack = (ev) => {
        console.log("received track");
    };
    return peerConnection;
}

async function beCallee(remoteOffer, peerConnection, username, dataChannel) {
    await receiveOfferSDP(peerConnection, remoteOffer);
    await sendAnswerSDP(peerConnection, username);

    try {
        dataChannel.obj = await waitForDataChannel(peerConnection);
    } catch (err) {
        console.log("waited too long for data channel. probably it was already received");
    } finally {
        dataChannel.obj.send("World");
        console.log("Sending message, check the other tab");
    }
}

async function receiveOfferSDP(peerConnection, remoteOffer) {
    await peerConnection.obj.setRemoteDescription(remoteOffer);
}

async function sendAnswerSDP(peerConnection, username) {
    await peerConnection.obj.setLocalDescription();

    const localAnswerWithICECandidates = peerConnection.obj.localDescription;

    // Send SDP through WebSocket instead of HTTP
    socket.send(JSON.stringify({
        "type": "sdp",
        "user": username,
        "sdp": localAnswerWithICECandidates
    }));
}

function waitForDataChannel(peerConnection) {
    return common.waitForEvent((fulfill) => {
        peerConnection.obj.ondataChannel = function (e) {
            const dataChannel = e.channel;
            dataChannel.onmessage = function (e) {
                console.log("Received message:", e.data);
            };
            fulfill(dataChannel);
        };
    });
}

async function beCaller(remoteAnswer, peerConnection, dataChannel) {
    await receiveAnswerSDP(peerConnection, remoteAnswer);
    await sendMessage(dataChannel);
}

async function receiveAnswerSDP(peerConnection) {
    peerConnection.obj.setRemoteDescription(remoteAnswer);
}

async function sendMessage(dataChannel) {
    if (secondOfferIsJustWithVideoTracks(dataChannel))
        await waitForDataChannelOpen(dataChannel);
    console.log("Sending message. Check the other tab");
    dataChannel.send("Hello");
}

function secondOfferIsJustWithVideoTracks() {
    return dataChannel.obj !== null && dataChannel.obj.readyState !== "open";
}

function waitForDataChannelOpen(dataChannel) {
    return common.waitForEvent((fulfill) => {
        dataChannel.obj.onopen = function () {
            if (dataChannel.obj.readyState == "open") {
                fulfill();
            }
        };
    });
}

function withPerfectNegociationHandler(user_function, peerConnection, username, dataChannel) {
    var makingOffer = { obj: false };

    addNegotiationNeededHandler(peerConnection, makingOffer, username);

    var es = new ReconnectingEventSource('/events?channel=testchannel');
    es.addEventListener('message', async function ({ data }) {
        try {
            if (shouldSkipMessage(data, peerConnection, username, makingOffer)) {
                return;
            }
            if (peerRefreshedPage(dataChannel) || shouldAcceptOffer(username, peerConnection)) {
                console.log("Reinitialized RTCPeerConnection");
                peerConnection.obj.close();
                peerConnection.obj = initializeRTCPeerConnection();
                addNegotiationNeededHandler(peerConnection, makingOffer, username);
            }

            const SDP = JSON.parse(data).sdp;
            await user_function(SDP);
        } catch (err) {
            console.error(err);
        }
    }, false);
    return makingOffer;
}

function handleSDP(sdp, username) {
    // Handle incoming SDP offer/answer
    const description = new RTCSessionDescription(sdp);
    if (description.type === "offer") {
        // Process as offer
    } else if (description.type === "answer") {
        // Process as answer
    }
}

function shouldSkipMessage(data, peerConnection, username, makingOffer) {
    const message = JSON.parse(data);
    if (messageIsReflected(message, username))
        return true;
    const description = JSON.parse(message.sdp);
    if (shouldIgnoreOffer(description, makingOffer, peerConnection.username))
        return true;
    return false;
}

function messageIsReflected(message, username) {
    return message.user === username;
}

function shouldIgnoreOffer(description, makingOffer, peerConnection, username) {
    const offerCollision = (description.type === "offer") && (makingOffer.obj || peerConnection.obj.signalingState !== "stable");
    const shouldIgnore = (username === "impolite") && offerCollision;
    return shouldIgnore;
}

function peerRefreshedPage(dataChannel) {
    return dataChannel.obj !== null && (dataChannel.obj.readyState === "closing" || dataChannel.obj.readyState === "closed");
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function addNegotiationNeededHandler(peerConnection, makingOffer, username) {
    var collectedIce = false;
    peerConnection.obj.onnegotiationneeded = async () => {
        try {
            makingOffer.obj = true;
            await peerConnection.obj.setLocalDescription();
            if (!collectedIce) {
                await common.waitForAllICE(peerConnection);
                collectedIce = true;
            }

            const localOfferWithICECandidates = peerConnection.obj.localDescription;
            socket.send(JSON.stringify({
                "type": "sdp",
                "user": username,
                "sdp": localOfferWithICECandidates
            }));
        } catch (err) {
            console.log(err);
        } finally {
            makingOffer.obj = false;
        }
    };
}

async function secondNegotiationNeededEvent(peerConnection) {
    peerConnection.obj.createDataChannel("chat2");

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: true });
    for (const track of stream.getTracks()) {
        peerConnection.obj.addTrack(track, stream);
    }
    console.log("Should fire new negotiationneeded event");
}

function firstNegotiationNeededEvent(peerConnection, dataChannel) {
    dataChannel.obj = peerConnection.obj.createDataChannel(common.CHAT_CHANNEL);
    dataChannel.obj.onmessage = function (e) {
        console.log("Received message:", e.data);
    };
}
*/
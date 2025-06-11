const username = JSON.parse(document.getElementById('user-username').textContent);
const ws = new WebSocket('ws://' + window.location.host + '/ws/videochat/');
const peerConnections = {};
const remoteStreams = {};
let localStream;

// Initialize video chat
async function init() {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    document.getElementById('localVideo').srcObject = localStream;
}

function createPeerConnection(peerUsername) {
    const pc = new RTCPeerConnection({
        iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    });

    localStream.getTracks().forEach(track => {
        pc.addTrack(track, localStream);
    });

    pc.onicecandidate = (event) => {
        if (event.candidate) {
            ws.send(JSON.stringify({
                type: 'ice',
                target: peerUsername,
                sender: username,
                candidate: event.candidate
            }));
        }
    };

    pc.ontrack = (event) => {
        if (!remoteStreams[peerUsername]) {
            remoteStreams[peerUsername] = new MediaStream();
            const remoteVideo = document.createElement('video');
            remoteVideo.id = `video-${peerUsername}`;
            remoteVideo.autoplay = true;
            remoteVideo.playsInline = true;
            remoteVideo.srcObject = remoteStreams[peerUsername];
            document.getElementById('remoteVideos').appendChild(remoteVideo);
        }
        remoteStreams[peerUsername].addTrack(event.track);
    };

    return pc;
}

// Handle incoming WebSocket messages
ws.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    const { type, sender, target, sdp, candidate } = data;

    if (sender === username) return;

    if (!peerConnections[sender]) {
        peerConnections[sender] = createPeerConnection(sender);
    }

    const pc = peerConnections[sender];

    if (type === 'offer') {
        await pc.setRemoteDescription(new RTCSessionDescription(sdp));
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        ws.send(JSON.stringify({
            type: 'answer',
            target: sender,
            sender: username,
            sdp: pc.localDescription
        }));
    }

    if (type === 'answer') {
        await pc.setRemoteDescription(new RTCSessionDescription(sdp));
    }

    if (type === 'ice' && candidate) {
        try {
            await pc.addIceCandidate(new RTCIceCandidate(candidate));
        } catch (err) {
            console.error('Error adding ICE:', err);
        }
    }
};

ws.onopen = () => {
    console.log('✅ WebSocket connected');
    ws.send(JSON.stringify({ type: 'join', sender: username }));
};

async function callUser(peerUsername) {
    if (!peerConnections[peerUsername]) {
        peerConnections[peerUsername] = createPeerConnection(peerUsername);
    }

    const pc = peerConnections[peerUsername];
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    ws.send(JSON.stringify({
        type: 'offer',
        target: peerUsername,
        sender: username,
        sdp: pc.localDescription
    }));
}

window.onload = async () => {
    await init();
};
export const CHAT_CHANNEL = 'test_chat';

export function waitForAllICE(peerConnection) {
    return waitForEvent((fulfill) => {
        peerConnection.onicecandidate = (iceEvent) => {
            if (iceEvent.candidate === null) fulfill();
        };
    });
}

export function waitForEvent(user_function) {
    return new Promise((fulfill, reject) => {
        user_function(fulfill);
        setTimeout(() => reject("Waited too long"), 60000);
    });
}

export function addConnectionStateHandler(peerConnection, username) {
    window.onbeforeunload = function () {
        retrieveOffer(username);
    };

    peerConnection.onconnectionstatechange = function () {
        const state = peerConnection.connectionState;  // Correct property name
        console.log(state);
        if (state === "disconnected" || state === "failed") {
            retrieveOffer(username);
        } else if (state === "connected") {
            clearBothOffers(username);  // Updated function usage
        }
    };
}

// Declare clearBothOffers here only once
const clearBothOffers = (username) => {
    fetch('http://127.0.0.1:8000/offer', {
        method: "POST",
        body: JSON.stringify({ user: username, offer: '' }),
        headers: { 'Content-Type': 'application/json' }
    });
};

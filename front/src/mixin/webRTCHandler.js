import * as constants from './constants.js';

let connectedUserDetails;

export const sendPreOffer = (callType, calleePersonalCode) => {
  console.log("webRTCHandler.sendPreOffer()...")
  connectedUserDetails = {
    callType,
    socketId: calleePersonalCode,
  };

  if (callType === constants.callType.CHAT_PERSONAL_CODE || callType === constants.callType.VIDEO_PERSONAL_CODE) {
    const data = {
      callType,
      calleePersonalCode,
    };
    //ui.showCallingDialog(callingDialogRejectCallHandler);
    //wss.sendPreOffer(data);
  }
};

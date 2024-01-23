function showSuccessNotification(message) {
    iziToast.success({
        title: "OK",
        message: message,
        timeout: 5000,
        position: "topCenter"
    });
//    iziToast.show({
//        theme: "light",
//        color: "green",
//        title: status,
//        message: message,
//        timeout: 5000,
//        position: "topCenter"
//    });
}


function showInfoNotification(message) {
    iziToast.info({
        title: "Hello",
        message: message,
        timeout: 5000,
        position: "topCenter"
    });
//    iziToast.show({
//        theme: "light",
//        color: "blue",
//        title: status,
//        message: message,
//        timeout: 5000,
//        position: "topCenter"
//    });
}


function showWarningNotification(message) {
    iziToast.warning({
        title: "Caution",
        message: message,
        timeout: 5000,
        position: "topCenter"
    });
//    iziToast.show({
//        theme: "light",
//        color: "yellow",
//        title: status,
//        message: message,
//        timeout: 5000,
//        position: "topCenter"
//    });
}


function showErrorNotification(message) {
    iziToast.error({
        title: "Error",
        message: message,
        timeout: 5000,
        position: "topCenter"
    });
//    iziToast.show({
//        theme: "light",
//        color: "red",
//        title: status,
//        message: message,
//        timeout: 5000,
//        position: "topCenter"
//    });
}

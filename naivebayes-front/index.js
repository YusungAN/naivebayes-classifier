

const enterkey = async (e) => {
    if (e.keyCode === 13) {
        await sendData();
    }
};

const sendData = async () => {
    document.getElementById("isbias").innerHTML = "음......";
    const data = document.getElementById("input").value;
    const {
        data: { success, desc },
    } = await axios.post("https://anyusung.me/api/checkbayes", {sentence: data});
    if (success) {
        if (desc === "True\n") {
            document.getElementById("isbias").innerHTML = "악플인거 같아요";
        } else if (desc === "False\n") {
            document.getElementById("isbias").innerHTML =
                "악플이 아닌거 같아요";
        }
    }
};

document.addEventListener("keypress", enterkey);

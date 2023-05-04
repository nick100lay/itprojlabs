
import axios from "axios"


export function defaultPostMethod(url, newData, json, setJson) {
    return axios
        .post(url, newData)
        .then((resp) => setJson([...json, ...resp.data]))
}
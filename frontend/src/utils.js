export const FetchReport = async (kwargs) => {
    let response
    const url = `http://localhost:8000/api/summary`
    fetch(url, {
        method:"POST",
        headers:{
            'Content-Type': "application/json"
        },
        body: JSON.stringify(kwargs)
    })
    .then(res => res.json())
    .then(result => result = response)
    return response
};

export const FormatResponse = (response) => {
    const overall = Number(response.unknown) + Number(response.up) + Number(response.down)
    let unk = (overall-Number(response.up) - Number(response.down))/overall
    let u = (overall-Number(response.unknown) - Number(response.down))/overall
    let d = (overall-Number(response.up) - Number(response.unknown))/overall
    return {
        'unknown': unk,
        'up': u,
        'down': d 
    }
};
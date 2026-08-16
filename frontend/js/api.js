const API_BASE = "http://127.0.0.1:5000/api";

async function apiRequest(path, method = "GET", body = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include"
    };

    if (body !== null) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}${path}`, options);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
    }

    return data;
}


// =========================
// AUTH API
// =========================

const AuthAPI = {
    register: (fullName, email, password) =>
        apiRequest(
            "/auth/register",
            "POST",
            {
                full_name: fullName,
                email,
                password
            }
        ),

    login: (email, password) =>
        apiRequest(
            "/auth/login",
            "POST",
            {
                email,
                password
            }
        ),

    logout: () =>
        apiRequest("/auth/logout", "POST"),

    me: () =>
        apiRequest("/auth/me", "GET"),

    updateProfile: (payload) =>
        apiRequest("/auth/profile", "PUT", payload)
};


// =========================
// FARM API
// =========================

const FarmAPI = {
    list: () =>
        apiRequest("/farms", "GET"),

    create: (farm) =>
        apiRequest("/farms", "POST", farm),

    update: (id, farm) =>
        apiRequest(`/farms/${id}`, "PUT", farm),

    remove: (id) =>
        apiRequest(`/farms/${id}`, "DELETE")
};


// =========================
// HISTORY API
// =========================

const HistoryAPI = {

    cropList: (farmId) =>
        apiRequest(
            `/farms/${farmId}/crop-history`,
            "GET"
        ),

    cropCreate: (farmId, data) =>
        apiRequest(
            `/farms/${farmId}/crop-history`,
            "POST",
            data
        ),

    cropDelete: (farmId, id) =>
        apiRequest(
            `/farms/${farmId}/crop-history/${id}`,
            "DELETE"
        ),


    fertilizerList: (farmId) =>
        apiRequest(
            `/farms/${farmId}/fertilizer-history`,
            "GET"
        ),

    fertilizerCreate: (farmId, data) =>
        apiRequest(
            `/farms/${farmId}/fertilizer-history`,
            "POST",
            data
        ),

    fertilizerDelete: (farmId, id) =>
        apiRequest(
            `/farms/${farmId}/fertilizer-history/${id}`,
            "DELETE"
        ),


    diseaseList: (farmId) =>
        apiRequest(
            `/farms/${farmId}/disease-history`,
            "GET"
        ),

    diseaseCreate: (farmId, data) =>
        apiRequest(
            `/farms/${farmId}/disease-history`,
            "POST",
            data
        ),

    diseaseDelete: (farmId, id) =>
        apiRequest(
            `/farms/${farmId}/disease-history/${id}`,
            "DELETE"
        )
};


// =========================
// WEATHER API
// =========================

const WeatherAPI = {
    get: (location) =>
        apiRequest(
            `/weather?location=${encodeURIComponent(location)}`,
            "GET"
        )
};


// =========================
// MARKET API
// =========================

const MarketAPI = {
    get: (state, commodity) => {

        const params = new URLSearchParams();

        if (state) {
            params.append("state", state);
        }

        if (commodity) {
            params.append("commodity", commodity);
        }

        const query = params.toString();

        return apiRequest(
            `/market-prices?${query}`,
            "GET"
        );
    }
};


// =========================
// NOTIFICATION API
// =========================

const NotificationAPI = {

    list: () =>
        apiRequest(
            "/notifications",
            "GET"
        ),

    markRead: (id) =>
        apiRequest(
            `/notifications/${id}/read`,
            "PATCH"
        ),

    remove: (id) =>
        apiRequest(
            `/notifications/${id}`,
            "DELETE"
        )
};


// =========================
// ANALYTICS API
// =========================

const AnalyticsAPI = {
    get: () =>
        apiRequest(
            "/analytics",
            "GET"
        )
};


// =========================
// ADMIN API
// =========================

const AdminAPI = {

    stats: () =>
        apiRequest(
            "/admin/stats",
            "GET"
        ),

    farmers: () =>
        apiRequest(
            "/admin/farmers",
            "GET"
        ),

    datasets: () =>
        apiRequest(
            "/admin/datasets",
            "GET"
        ),

    deactivateFarmer: (id) =>
        apiRequest(
            `/admin/farmers/${id}/deactivate`,
            "PATCH"
        ),

    promoteFarmer: (id) =>
        apiRequest(
            `/admin/farmers/${id}/promote`,
            "PATCH"
        )
};


// =========================
// CROP RECOMMENDATION API
// =========================

const CropAPI = {

    recommend: (data) =>
        apiRequest(
            "/crop-recommendation",
            "POST",
            data
        )
};


// =========================
// FERTILIZER API
// =========================

const FertilizerAPI = {

    options: () =>
        apiRequest(
            "/fertilizer-recommendation/options",
            "GET"
        ),

    recommend: (data) =>
        apiRequest(
            "/fertilizer-recommendation",
            "POST",
            data
        )
};


// =========================
// YIELD API
// =========================

const YieldAPI = {

    options: () =>
        apiRequest(
            "/yield-prediction/options",
            "GET"
        ),

    predict: (data) =>
        apiRequest(
            "/yield-prediction",
            "POST",
            data
        )
};


// =========================
// PEST PREDICTION API
// =========================

const PestAPI = {

    predict: async (imageFile) => {

        console.log("PestAPI: starting request");

        const formData = new FormData();

        formData.append("image", imageFile);


        const response = await fetch(
            `${API_BASE}/pest-prediction`,
            {
                method: "POST",
                credentials: "include",
                body: formData
            }
        );


        console.log(
            "PestAPI: response status =",
            response.status
        );


        const text = await response.text();


        console.log(
            "PestAPI: response body =",
            text
        );


        if (!response.ok) {

            throw new Error(
                text || `Server error: ${response.status}`
            );
        }


        if (!text) {

            throw new Error(
                "Server returned an empty response."
            );
        }


        let data;

        try {

            data = JSON.parse(text);

        } catch (error) {

            throw new Error(
                "Invalid JSON returned by server: " + text
            );
        }


        return data;
    }
};
const IrrigationAPI = {
  options: () => apiRequest("/irrigation/options", "GET"),
  recommend: (data) => apiRequest("/irrigation", "POST", data)
};
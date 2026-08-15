console.log("Pest.js loaded");

document.addEventListener("DOMContentLoaded", () => {

    console.log("DOM loaded");

    const uploadZone = document.getElementById("uploadZone");
    const fileInput = document.getElementById("pestImageInput");
    const preview = document.getElementById("imagePreview");
    const prompt = document.getElementById("uploadPrompt");
    const submitBtn = document.getElementById("pestSubmitBtn");
    const resultEl = document.getElementById("pestResult");

    console.log("Elements:", {
        uploadZone,
        fileInput,
        preview,
        prompt,
        submitBtn,
        resultEl
    });

    let selectedImageFile = null;


    // =========================
    // SELECT IMAGE
    // =========================

    uploadZone.addEventListener("click", () => {

        console.log("Upload zone clicked");

        fileInput.click();
    });


    fileInput.addEventListener("change", () => {

        console.log("File input changed");

        const file = fileInput.files[0];

        if (!file) {
            console.log("No file selected");
            return;
        }

        console.log("Selected file:", file.name);

        selectedImageFile = file;

        // Show preview
        const reader = new FileReader();

        reader.onload = (event) => {

            preview.src = event.target.result;

            preview.style.display = "block";

            prompt.style.display = "none";
        };

        reader.readAsDataURL(file);


        // Enable button
        submitBtn.disabled = false;

        console.log(
            "Button enabled:",
            !submitBtn.disabled
        );

        resultEl.innerHTML = "";
    });


    // =========================
    // IDENTIFY PEST
    // =========================

    submitBtn.addEventListener("click", async () => {

        console.log("IDENTIFY BUTTON CLICKED");


        if (!selectedImageFile) {

            resultEl.innerHTML = `
                <div style="color:red;">
                    Please select an image first.
                </div>
            `;

            return;
        }


        console.log(
            "Selected image:",
            selectedImageFile.name
        );


        // Show loading
        submitBtn.disabled = true;

        submitBtn.textContent = "Identifying...";

        resultEl.innerHTML = `
            <div style="
                color:orange;
                padding:20px;
                font-size:16px;
            ">
                Sending image to server...
            </div>
        `;


        try {

            console.log("Calling PestAPI.predict()");


            // IMPORTANT
            const result =
                await PestAPI.predict(selectedImageFile);


            console.log(
                "Pest API returned:",
                result
            );


            // Validate result
            if (!result) {

                throw new Error(
                    "Server returned no result."
                );
            }


            if (!result.predicted_pest) {

                throw new Error(
                    "Server response does not contain predicted_pest."
                );
            }


            // =========================
            // SUCCESS
            // =========================

            resultEl.innerHTML = `
                <div
                    class="card fade-in-up"
                    style="
                        padding:32px;
                        max-width:560px;
                        text-align:center;
                        margin:20px auto;
                    "
                >

                    <div style="
                        font-family:var(--font-mono);
                        font-size:0.75rem;
                        text-transform:uppercase;
                        color:var(--color-text-faint);
                        letter-spacing:0.06em;
                        margin-bottom:12px;
                    ">
                        Identified Pest
                    </div>


                    <div style="
                        font-family:var(--font-display);
                        font-size:2.2rem;
                        font-weight:600;
                        color:var(--color-green);
                        text-transform:capitalize;
                        margin-bottom:12px;
                    ">
                        🐛 ${result.predicted_pest}
                    </div>


                    <div style="
                        color:var(--color-text-dim);
                        font-size:0.9rem;
                    ">
                        ${result.confidence}% model confidence
                    </div>

                </div>
            `;


            console.log(
                "RESULT DISPLAYED SUCCESSFULLY"
            );


        } catch (error) {

            console.error(
                "PEST PREDICTION ERROR:",
                error
            );


            // DO NOT HIDE THE ERROR
            resultEl.innerHTML = `
                <div
                    class="card"
                    style="
                        padding:25px;
                        margin-top:20px;
                        border:1px solid red;
                    "
                >

                    <h2 style="color:red;">
                        ⚠️ Pest Prediction Error
                    </h2>

                    <p style="
                        color:var(--color-text-dim);
                        margin-top:10px;
                    ">
                        ${error.message}
                    </p>

                </div>
            `;
        }


        // Re-enable button
        submitBtn.disabled = false;

        submitBtn.textContent = "Identify Pest";


        console.log(
            "Prediction process finished"
        );

    });

});
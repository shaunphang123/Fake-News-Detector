<script>
import axios from 'axios'
export default {
    setup() {
        if (!localStorage.getItem('pastPredictions')) {
            localStorage.setItem('pastPredictions', JSON.stringify([]))
        }
        console.log(localStorage.getItem('pastPredictions'))
    },
    data: () => ({
        loaded: false,
        loading: false,
        article: '',
        rules: {
            required: value => !!value || 'Field is required',
        },
        snackbar: false,
        prediction_score: 0,
        prediction_article: '',
    }),

    methods: {
        onClick () {
            if (!this.article) {
                this.snackbar = true
                this.text = 'Please fill out the form'
                return
            }
            this.loading = true
            console.log(1)

            axios.post('http://localhost:5000/predict', {
                article: this.article
            })
            .then((response) => {
                console.log(response)
                this.prediction_score = response.data.prediction.score
                this.prediction_article = response.data.prediction.article
            })
            .catch((error) => {
                console.log(error)
            })
            .finally(() => {
                this.loading = false
                this.loaded = true
            })
        },
        savePrediction() {
            const pastPredictions = JSON.parse(localStorage.getItem('pastPredictions'))
            const newPastPredictions = [...pastPredictions, {
                article: this.article,
                prediction_score: this.prediction_score,
                prediction: this.prediction_score < 0.51 ? 'Most Likely True' : 'Most Likely False'
            }]
            localStorage.setItem('pastPredictions', JSON.stringify(newPastPredictions))
            this.snackbar = true
            this.text = 'Prediction saved'
            setTimeout(() => {
                window.location.reload()
            }, 1000);
        }
    },
}
</script>
<template>
    <v-container class="fill-height h-screen align-center justify-center" >
        <v-container class="position-absolute w-50">
            <v-text-field
                :loading="loading"
                v-model="article"
                clearable
                label="Headline/Article"
                variant="outlined"
                append-inner-icon="mdi-magnify"
                @click:append-inner="onClick"
                :rules="[rules.required]"
            ></v-text-field>
            
            <v-container v-if="loaded">
                <v-card :title="this.prediction_score < 0.51 ? 'Most Likely True' : 'Most Likely False'" :class="this.prediction_score < 0.51 ? 'bg-green' : 'bg-warning'" :subtitle="this.prediction_score < 0.51 ? 'This article is most likely truthful.' : 'This article/headline most likely has falsehoods or strong language to suggest that it is not truthful.'" v-if="loaded">
                    <v-card-text>
                        <blockquote class="font-italic">"{{ this.prediction_article }}"</blockquote>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn @click="savePrediction">Save Prediction</v-btn>
                    </v-card-actions>
                </v-card>
            </v-container>
        </v-container>
    </v-container>
    <v-snackbar
        v-model="snackbar"
        :timeout="timeout"
    >
        {{ text }}
        <template v-slot:actions>
            <v-btn
                color="blue"
                variant="text"
                @click="snackbar = false"
            >
                Close
            </v-btn>
        </template>
    </v-snackbar>
</template>
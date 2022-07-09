import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    selected: null,
    titleVerificationCompleted: false
};

export const appSlice = createSlice({
    name: "appState",
    initialState,
    reducers: {
        setSelectedName: (state, action) => {
            state.selected = action.payload;
        },
        setTitleVerificationCompleted: (state, action) => {
            state.titleVerificationCompleted = action.payload;

        },
    },
});

// Action creators are generated for each case reducer function
export const { setSelectedName, setTitleVerificationCompleted } = appSlice.actions;

export default appSlice.reducer;
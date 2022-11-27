import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { USERS_URL } from './constants';


const fetchIsTeammate = createAsyncThunk(
    'user/getIsTeammate',
    async (thunkAPI) => {
        const res = await fetch(USERS_URL + 'authorization_like_teammate/').then(
        (data) => data.json()
    )
    return res;
});

const fetchIsAdmin = createAsyncThunk(
    'user/getIsAdmin',
    async (thunkAPI) => {
        const res = await fetch(USERS_URL + 'authorization_like_admin/').then(
        (data) => data.json()
    )
    return res;
});

const fetchImage = createAsyncThunk(
    'user/getImage',
    async (thunkAPI) => {
        const res = await fetch(USERS_URL + 'authorization_like_creator/').then(
        (data) => data.json()
    )
    return res;
});

const initialState = {
    token: null,
    isTeammate: false,
    isAdmin: false,
    isCreator: false,
    image: "",
};


const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        userAdded(state, action) {
            state.push(action.payload);
        },
        userUpdated(state, action) {
            const {token, isTeammate, isAdmin, image} = action.payload;
            state.token = token;
            state.isTeammate = isTeammate;
            state.isAdmin = isAdmin;
            state.image = image;
        }
    },
    extraReducers: builder => {
        builder.addCase(fetchIsTeammate.fulfilled, (state, { payload }) => {
            state.isTeammate = payload;
        }),
        builder.addCase(fetchIsAdmin.fulfilled, (state, { payload }) => {
            state.isAdmin = payload;
        }),
        builder.addCase(fetchImage.fulfilled, (state, { payload }) => {
            state.image = payload;
        })
    }
})

export const { userAdded, userUpdated } = userSlice.actions;

export default userSlice.reducer;
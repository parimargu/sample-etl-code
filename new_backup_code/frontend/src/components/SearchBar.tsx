import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

interface SearchBarProps {
    onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{
            display: 'flex',
            gap: 2,
            maxWidth: 700,
            mx: 'auto',
            p: 1,
            bgcolor: 'background.paper',
            borderRadius: 4,
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
        }}>
            <TextField
                fullWidth
                variant="standard"
                placeholder="Search documents..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                InputProps={{
                    disableUnderline: true,
                    sx: { px: 2, py: 1, fontSize: '1.1rem' }
                }}
            />
            <Button
                variant="contained"
                type="submit"
                startIcon={<SearchIcon />}
                sx={{ px: 4, borderRadius: 3 }}
            >
                Search
            </Button>
        </Box>
    );
};

export default SearchBar;

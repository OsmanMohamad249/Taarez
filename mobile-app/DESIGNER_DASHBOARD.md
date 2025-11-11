# Designer Dashboard Implementation

This document describes the Flutter UI implementation for the Designer's Toolkit feature in the Tiraz mobile app.

## Overview

The Designer Dashboard provides a complete interface for users with the `DESIGNER` role to manage their design creations. It includes listing designs, adding new designs, and proper role-based navigation.

## Architecture

### Models

#### Design Model (`lib/models/design.dart`)
Updated to match backend schema:
- `name` (String) - Design name
- `base_price` (double) - Base price in SAR
- `base_image_url` (String?) - Optional image URL
- `description` (String?) - Optional description
- `style_type` (String?) - Optional style type
- `category_id` (String?) - Optional category ID
- `owner_id` (String) - Designer's user ID
- `is_active` (bool) - Active status
- `created_at` (DateTime) - Creation timestamp
- `customization_rules` (Map?) - Optional customization rules

Backward compatibility getters:
- `title` → `name`
- `price` → `base_price`
- `imageUrl` → `base_image_url`
- `designerId` → `owner_id`

#### Fabric Model (`lib/models/fabric.dart`)
- `id` (String) - Fabric ID
- `name` (String) - Fabric name
- `description` (String?) - Optional description
- `image_url` (String?) - Optional image
- `base_price` (double) - Base price

#### Color Model (`lib/models/color.dart`)
- `id` (String) - Color ID
- `name` (String) - Color name
- `hex_code` (String) - Color hex code (e.g., "#FF0000")

### Services

#### DesignService (`lib/services/design_service.dart`)
Extended with designer-specific methods:

**`getMyDesigns()`**
- Endpoint: `GET /designs/me`
- Returns: `Future<List<Design>>`
- Fetches designs owned by the authenticated designer
- Throws exception on error

**`createDesign()`**
- Endpoint: `POST /designs/`
- Parameters:
  - `name` (required): Design name
  - `description` (required): Design description
  - `basePrice` (required): Base price
  - `styleType` (optional): Style type
  - `baseImageUrl` (optional): Image URL
  - `categoryId` (optional): Category ID
- Returns: `Map<String, dynamic>` with success status and design data

### Providers

#### Design Provider (`lib/providers/design_provider.dart`)
Riverpod providers for state management:

**`designServiceProvider`**
- Provider for DesignService instance

**`myDesignsProvider`**
- FutureProvider that fetches designer's designs
- Auto-refreshes on invalidation
- Handles loading, data, and error states

**`designsRefreshProvider`**
- StateProvider for triggering manual refresh (future enhancement)

### Screens

#### DesignerDashboardScreen (`lib/screens/designs/designer_dashboard_screen.dart`)
Main hub for designers.

**Features:**
- Lists all designer's designs using Riverpod FutureProvider
- Empty state with helpful message
- Loading state with spinner
- Error state with retry button
- Pull-to-refresh functionality
- Floating Action Button to add new designs
- Logout button in app bar

**Layout:**
- AppBar with title "My Designs"
- Refresh and Logout action buttons
- ListView of DesignListItem widgets
- FloatingActionButton for adding designs

#### AddDesignScreen (`lib/screens/designs/add_design_screen.dart`)
Form to create new designs.

**Features:**
- Form with validation
- Three required fields:
  1. Design Name (min 3 chars)
  2. Description (min 10 chars)
  3. Base Price (must be > 0, SAR)
- Loading state during submission
- Success/error feedback via SnackBar
- Returns `true` on success to trigger dashboard refresh

**Validation:**
- Name: Required, min 3 characters
- Description: Required, min 10 characters
- Base Price: Required, must be a valid number > 0

### Widgets

#### DesignListItem (`lib/widgets/design_list_item.dart`)
Reusable widget for displaying a single design in a list.

**Layout:**
- Card with elevation
- ListTile with:
  - Leading: Icon (checkroom) with blue background
  - Title: Design name
  - Subtitle: Base price formatted as SAR currency
  - Trailing: Chevron right arrow
- Tappable (currently shows SnackBar, ready for detail navigation)

### Authentication & Navigation

#### Role-Based Routing
Updated files:
- `login_screen.dart`: Routes to Dashboard if designer, HomeScreen if customer
- `splash_screen.dart`: Routes based on stored user role on app start

**Flow:**
1. User logs in
2. Auth service fetches user profile with role
3. If `user.isDesigner` → DesignerDashboardScreen
4. Else → HomeScreen (CustomerHomeScreen)

## API Integration

### Endpoints Used

**GET /designs/me**
- Authentication: Required (Bearer token)
- Authorization: Designer role required
- Response: Array of design objects
- Used by: `myDesignsProvider`

**POST /designs/**
- Authentication: Required (Bearer token)
- Authorization: Designer role required
- Body:
  ```json
  {
    "name": "Design Name",
    "description": "Description",
    "base_price": 350.0,
    "style_type": "optional",
    "base_image_url": "optional",
    "category_id": "optional"
  }
  ```
- Response: Created design object
- Used by: AddDesignScreen

## User Experience

### Empty State
When designer has no designs:
- Large icon (design_services_outlined)
- Message: "You haven't added any designs yet."
- Call to action: "Tap '+' to create your first one!"

### Loading State
- Centered CircularProgressIndicator
- Shown while fetching data

### Error State
- Error icon (red)
- Message: "Failed to load designs."
- Sub-message: "Please try again."
- Retry button with refresh icon

### Success Feedback
- Green SnackBar: "Design created successfully!"
- Auto-dismisses and returns to dashboard

### Error Feedback
- Red SnackBar with error message
- Stays visible until dismissed

## Currency Formatting

All prices displayed using `Helpers.formatCurrency()`:
- Format: "SAR XXX.XX"
- Example: "Starts at SAR 350.00"
- Uses intl package for proper formatting

## Future Enhancements

Ready for:
1. Design detail screen (tappable list items)
2. Edit design functionality
3. Delete design functionality
4. Image upload for designs
5. Category selection dropdown
6. Fabric and color selection
7. Design preview/visualization
8. Search and filter designs
9. Sort by various criteria

## Testing Checklist

- [ ] Designer can log in and see Dashboard
- [ ] Customer sees different home screen
- [ ] Empty state displays correctly
- [ ] Add design form validates all fields
- [ ] Design is created successfully
- [ ] Dashboard refreshes after adding design
- [ ] Logout works from Dashboard
- [ ] Error handling works for network failures
- [ ] Role-based navigation works on app restart

## Dependencies

No new dependencies added. Uses existing:
- `flutter_riverpod` - State management
- `http` - API calls
- `flutter_secure_storage` - Token storage
- `intl` - Currency formatting

## File Structure

```
mobile-app/lib/
├── models/
│   ├── design.dart (updated)
│   ├── fabric.dart (new)
│   └── color.dart (new)
├── services/
│   └── design_service.dart (updated)
├── providers/
│   └── design_provider.dart (new)
├── screens/
│   ├── auth/
│   │   ├── login_screen.dart (updated)
│   │   └── splash_screen.dart (updated)
│   └── designs/
│       ├── designer_dashboard_screen.dart (new)
│       └── add_design_screen.dart (new)
└── widgets/
    └── design_list_item.dart (new)
```

## Code Quality

- Follows Flutter best practices
- Uses Riverpod for state management
- Proper error handling
- Loading states for all async operations
- Form validation
- Responsive UI
- Consistent styling
- Clean separation of concerns
- No hardcoded values where possible

## Security

- JWT token required for all API calls
- Role-based access enforced by backend
- No sensitive data in UI
- Secure token storage via flutter_secure_storage
- Proper error messages (no stack traces to users)

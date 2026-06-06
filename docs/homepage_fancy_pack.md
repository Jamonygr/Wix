# Homepage Fancy Pack

This package adds the homepage upgrades suggested for Beyond Cloud with Chriz:

- CTA mission panel
- animated cloud terminal
- Start Here card grid
- curated latest Azure posts section
- newsletter request panel
- optional mobile/custom-code polish

## Files

| File | Use |
| --- | --- |
| `components/homepage_fancy_pack.html` | Main all-in-one Wix HTML embed section. |
| `components/homepage_mobile_polish_custom_code.html` | Optional Wix Custom Code snippet for page-wide mobile/hover polish. |

## Wix Placement

1. Open the Wix editor.
2. Add an HTML embed section below the existing hero image or below the challenge section.
3. Paste the full contents of `components/homepage_fancy_pack.html`.
4. Set the embed width to full page width.
5. Start with an embed height around `2300px` on desktop.
6. Check mobile layout and adjust the embed height if Wix clips the bottom.

## Optional Mobile Polish

The mobile polish file must be added through Wix Dashboard custom code because normal HTML embeds usually run inside an iframe and cannot style the parent Wix page.

1. Go to Wix Dashboard.
2. Open Settings.
3. Open Custom Code.
4. Add a new code snippet in the Head.
5. Paste `components/homepage_mobile_polish_custom_code.html`.
6. Apply it to the homepage first.

## Links Used

- GitHub Labz: `https://www.beyondcloudwithchriz.com/githublabz`
- Azure Certification Paths: `https://www.beyondcloudwithchriz.com/azurecertificationpaths`
- Terraform Azure: `https://www.beyondcloudwithchriz.com/terraformazure`
- Blog/home feed: `https://www.beyondcloudwithchriz.com/`

## Notes

The newsletter panel opens a prefilled email to `info@beyondcloudwithchriz.com`. If you want full Wix Contacts integration later, connect this design to a native Wix form or Velo endpoint.

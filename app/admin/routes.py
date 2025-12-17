@admin_bp.route("/approve-venue/<int:venue_id>", methods=["POST"])
@login_required("admin")
def approve_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    venue.is_approved = True
    db.session.commit()
    return redirect("/admin/dashboard")

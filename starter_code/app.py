# Imports
import json
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import *
from forms import *
from datetime import datetime

# App Config.
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

# Filters.
@app.template_filter('datetime')
def format_datetime(value, format='medium'):
    date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return date.strftime(format)

# Customized Functions
def search(db_class, skey):
    data = []
    results = db.session.query(db_class).filter(
        db_class.name.ilike(f'%{skey}%') |
        db_class.city.ilike(f'%{skey}%') |
        db_class.state.ilike(f'%{skey}%')
    ).all()
    for result in results:
        data.append({
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": len(result.upcoming_shows)
        })
    results_data = {
        "count": len(results),
        "data": data
    }
    return results_data

# Controllers.
@app.route('/')
def index():
    return render_template('pages/home.html')

# Venues
@app.route('/venues')
def venues():
    data = []
    groups = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
    if not groups:
        flash('No venues exist')
        return render_template('pages/venues.html')
    for group in groups:
        venues = Venue.query.filter_by(city=group[0], state=group[1]).all()
        venues_list = []
        for venue in venues:
            venues_list.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(venue.upcoming_shows)
            })
        data.append({
            "city": group[0],
            "state": group[1],
            "venues": venues_list,
        })
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    return render_template('pages/search_venues.html', results=search(Venue, request.form.get('search_term', '')), search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=venue)

# Create Venue
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        try:
            name_reserved = Venue.query.filter_by(name=form.name.data).first()
            if name_reserved:
                flash('Venue name reserved')
                return render_template('forms/new_venue.html', form=form)
            new_venue = Venue()
            form.populate_obj(new_venue)
            db.session.add(new_venue)
            db.session.commit()
            flash('Venue ' + form.name.data + ' was successfully created!')
        except:
            flash('An error occurred. Venue ' + form.name.data + ' could not be created.')
            db.session.rollback()
        finally:
            db.session.close()
        return redirect('/')
    else:
        return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<int:venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        flash('Venue was successfully deleted with all of its shows.')
    except:
        flash('Venue could not be deleted. An error occurred!')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect('/')

# Artists
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    return render_template('pages/search_artists.html', results=search(Artist, request.form.get('search_term', '')), search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist)

# Create Artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if form.validate_on_submit():
        try:
            name_reserved = Artist.query.filter_by(name=form.name.data).first()
            if name_reserved:
                flash('Artist name reserved')
                return render_template('forms/new_artist.html', form=form)
            new_artist = Artist()
            form.populate_obj(new_artist)
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + form.name.data + ' was successfully listed!')
        except:
            flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
            db.session.rollback()
        finally:
            db.session.close()
        return redirect('/')
    else:
        return render_template('forms/new_artist.html', form=form)

# Update Artist
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)
    if form.validate_on_submit():
        try:
            form.populate_obj(artist)
            db.session.commit()
            flash('Artist was successfully updated!')
            return redirect(url_for('show_artist', artist_id=artist_id))
        except:
            flash('Oops! Something went wrong, the update was unsuccessful!')
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('forms/edit_artist.html', form=form, artist=artist)

# Update Venue
@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)
    if form.validate_on_submit():
        try:
            form.populate_obj(venue)
            db.session.commit()
            flash('Venue was successfully updated!')
            return redirect(url_for('show_venue', venue_id=venue_id))
        except:
            flash('Oops! Something went wrong, the update was unsuccessful!')
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('forms/edit_venue.html', form=form, venue=venue)

# Shows
@app.route('/shows')
def shows():
    shows = Show.query.all()
    return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create', methods=['GET', 'POST'])
def create_show():
    form = ShowForm()
    if form.validate_on_submit():
        try:
            new_show = Show()
            form.populate_obj(new_show)
            db.session.add(new_show)
            db.session.commit()
            flash('Show was successfully listed!')
            return redirect(url_for('shows'))
        except:
            flash('An error occurred. Show could not be listed.')
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('forms/new_show.html', form=form)

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run()
